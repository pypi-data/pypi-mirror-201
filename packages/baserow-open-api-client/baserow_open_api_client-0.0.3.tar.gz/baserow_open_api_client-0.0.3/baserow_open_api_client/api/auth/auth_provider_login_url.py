from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.auth_provider_login_url_response_200 import AuthProviderLoginUrlResponse200
from ...models.auth_provider_login_url_response_400 import AuthProviderLoginUrlResponse400
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/sso/saml/login-url/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["email"] = email

    params["group_invitation_token"] = group_invitation_token

    params["language"] = language

    params["original"] = original

    params["workspace_invitation_token"] = workspace_invitation_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    result = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AuthProviderLoginUrlResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AuthProviderLoginUrlResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Response[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    """Return the correct redirect_url to initiate the SSO SAML login. It needs an email address if
    multiple SAML providers are configured otherwise the only configured SAML provider signup URL will
    be returned.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]
    """

    kwargs = _get_kwargs(
        client=client,
        email=email,
        group_invitation_token=group_invitation_token,
        language=language,
        original=original,
        workspace_invitation_token=workspace_invitation_token,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    """Return the correct redirect_url to initiate the SSO SAML login. It needs an email address if
    multiple SAML providers are configured otherwise the only configured SAML provider signup URL will
    be returned.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]
    """

    return sync_detailed(
        client=client,
        email=email,
        group_invitation_token=group_invitation_token,
        language=language,
        original=original,
        workspace_invitation_token=workspace_invitation_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Response[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    """Return the correct redirect_url to initiate the SSO SAML login. It needs an email address if
    multiple SAML providers are configured otherwise the only configured SAML provider signup URL will
    be returned.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]
    """

    kwargs = _get_kwargs(
        client=client,
        email=email,
        group_invitation_token=group_invitation_token,
        language=language,
        original=original,
        workspace_invitation_token=workspace_invitation_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]]:
    """Return the correct redirect_url to initiate the SSO SAML login. It needs an email address if
    multiple SAML providers are configured otherwise the only configured SAML provider signup URL will
    be returned.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AuthProviderLoginUrlResponse200, AuthProviderLoginUrlResponse400]
    """

    return (
        await asyncio_detailed(
            client=client,
            email=email,
            group_invitation_token=group_invitation_token,
            language=language,
            original=original,
            workspace_invitation_token=workspace_invitation_token,
        )
    ).parsed
