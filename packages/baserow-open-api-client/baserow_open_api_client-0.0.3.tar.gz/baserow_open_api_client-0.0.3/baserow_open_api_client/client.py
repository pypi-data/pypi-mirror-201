import ssl
from typing import Dict, Optional, Union

import attr
import httpx


@attr.s(auto_attribs=True)
class Client:
    """A class for keeping track of data related to the API

    Attributes:
        base_url: The base URL for the API, all requests are made to a relative path to this URL
        cookies: A dictionary of cookies to be sent with every request
        headers: A dictionary of headers to be sent with every request
        timeout: The maximum amount of a time in seconds a request can take. API functions will raise
            httpx.TimeoutException if this is exceeded.
        verify_ssl: Whether or not to verify the SSL certificate of the API server. This should be True in production,
            but can be set to False for testing purposes.
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document.
        follow_redirects: Whether or not to follow redirects. Default value is False.
    """

    base_url: str
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    raise_on_unexpected_status: bool = attr.ib(False, kw_only=True)
    follow_redirects: bool = attr.ib(False, kw_only=True)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)


class AutoRefreshingJWTAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, base_url, access_token=None, refresh_token=None, email=None, password=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = base_url
        self.password = password
        self.email = email
        self.has_password_and_email = self.password is not None and self.email is not None
        if not self.has_password_and_email and self.refresh_token is None:
            raise ValueError("Either a password AND email must provided OR a refresh_token.")
        if bool(self.email) != bool(self.password):
            raise ValueError("If email is set so must password")

    def refresh_refresh_and_access_tokens(self):
        if self.has_password_and_email:
            auth_response = yield self.build_auth_request()
            if auth_response.status_code == 200:
                self.update_access_and_refresh_token(auth_response)

    def refresh_access_token(self):
        if self.refresh_token is not None:
            refresh_response = yield self.build_refresh_request()
            if refresh_response.status_code == 200:
                self.update_access_token(refresh_response)
            elif refresh_response.status_code == 401:
                refresh_response_data = refresh_response.json()
                if refresh_response_data.get("error") == "ERROR_INVALID_REFRESH_TOKEN":
                    yield from self.refresh_refresh_and_access_tokens()
        else:
            yield from self.refresh_refresh_and_access_tokens()

    def auth_flow(self, request):
        if self.access_token is None:
            yield from self.refresh_access_token()

        if self.access_token is None:
            raise RuntimeError("Failed to authenticate with the Baserow API to get an access_token")

        request.headers["Authorization"] = f"JWT {self.access_token}"
        response = yield request

        if response.status_code == 401:
            data = response.json()
            if data.get("error") == "ERROR_INVALID_ACCESS_TOKEN":
                yield from self.refresh_access_token()

                request.headers["Authorization"] = f"JWT {self.access_token}"
                yield request

    def build_refresh_request(self):
        return httpx.Request(
            "POST", url=self.base_url + "/api/user/token-refresh/", json={"refresh_token": self.refresh_token}
        )

    def build_auth_request(self):
        return httpx.Request(
            "POST", url=self.base_url + "/api/user/auth/", json={"email": self.email, "password": self.password}
        )

    def update_access_token(self, response):
        data = response.json()
        self.access_token = data["access_token"]

    def update_access_and_refresh_token(self, response):
        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]


class AuthenticatedClient(Client):
    def __init__(
        self,
        *args,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.auth = self._setup_auth(access_token, refresh_token, email, password)

    def _setup_auth(self, access_token, refresh_token, email, password):
        return AutoRefreshingJWTAuth(self.base_url, access_token, refresh_token, email=email, password=password)
