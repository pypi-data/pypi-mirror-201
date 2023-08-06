from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.facebook_auth_provider_model_auth_provider import FacebookAuthProviderModelAuthProvider
from ...models.git_hub_auth_provider_model_auth_provider import GitHubAuthProviderModelAuthProvider
from ...models.git_lab_auth_provider_model_auth_provider import GitLabAuthProviderModelAuthProvider
from ...models.google_auth_provider_model_auth_provider import GoogleAuthProviderModelAuthProvider
from ...models.open_id_connect_auth_provider_model_auth_provider import OpenIdConnectAuthProviderModelAuthProvider
from ...models.password_auth_provider_model_auth_provider import PasswordAuthProviderModelAuthProvider
from ...models.saml_auth_provider_model_auth_provider import SamlAuthProviderModelAuthProvider
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/admin/auth-provider/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> Union[
                "FacebookAuthProviderModelAuthProvider",
                "GitHubAuthProviderModelAuthProvider",
                "GitLabAuthProviderModelAuthProvider",
                "GoogleAuthProviderModelAuthProvider",
                "OpenIdConnectAuthProviderModelAuthProvider",
                "PasswordAuthProviderModelAuthProvider",
                "SamlAuthProviderModelAuthProvider",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_0 = (
                        PasswordAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_1 = (
                        SamlAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_2 = (
                        GoogleAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_3 = (
                        FacebookAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_4 = (
                        GitHubAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_authentication_provider_auth_provider_type_5 = (
                        GitLabAuthProviderModelAuthProvider.from_dict(data)
                    )

                    return componentsschemas_authentication_provider_auth_provider_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_authentication_provider_auth_provider_type_6 = (
                    OpenIdConnectAuthProviderModelAuthProvider.from_dict(data)
                )

                return componentsschemas_authentication_provider_auth_provider_type_6

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    """List all the available authentication providers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Union['FacebookAuthProviderModelAuthProvider', 'GitHubAuthProviderModelAuthProvider', 'GitLabAuthProviderModelAuthProvider', 'GoogleAuthProviderModelAuthProvider', 'OpenIdConnectAuthProviderModelAuthProvider', 'PasswordAuthProviderModelAuthProvider', 'SamlAuthProviderModelAuthProvider']]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    """List all the available authentication providers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[Union['FacebookAuthProviderModelAuthProvider', 'GitHubAuthProviderModelAuthProvider', 'GitLabAuthProviderModelAuthProvider', 'GoogleAuthProviderModelAuthProvider', 'OpenIdConnectAuthProviderModelAuthProvider', 'PasswordAuthProviderModelAuthProvider', 'SamlAuthProviderModelAuthProvider']]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    """List all the available authentication providers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Union['FacebookAuthProviderModelAuthProvider', 'GitHubAuthProviderModelAuthProvider', 'GitLabAuthProviderModelAuthProvider', 'GoogleAuthProviderModelAuthProvider', 'OpenIdConnectAuthProviderModelAuthProvider', 'PasswordAuthProviderModelAuthProvider', 'SamlAuthProviderModelAuthProvider']]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[
    List[
        Union[
            "FacebookAuthProviderModelAuthProvider",
            "GitHubAuthProviderModelAuthProvider",
            "GitLabAuthProviderModelAuthProvider",
            "GoogleAuthProviderModelAuthProvider",
            "OpenIdConnectAuthProviderModelAuthProvider",
            "PasswordAuthProviderModelAuthProvider",
            "SamlAuthProviderModelAuthProvider",
        ]
    ]
]:
    """List all the available authentication providers.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[Union['FacebookAuthProviderModelAuthProvider', 'GitHubAuthProviderModelAuthProvider', 'GitLabAuthProviderModelAuthProvider', 'GoogleAuthProviderModelAuthProvider', 'OpenIdConnectAuthProviderModelAuthProvider', 'PasswordAuthProviderModelAuthProvider', 'SamlAuthProviderModelAuthProvider']]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
