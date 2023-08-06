from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.public_view_auth_request import PublicViewAuthRequest
from ...models.public_view_auth_response import PublicViewAuthResponse
from ...models.public_view_token_auth_response_404 import PublicViewTokenAuthResponse404
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: PublicViewAuthRequest,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{slug}/public/auth/".format(client.base_url, slug=slug)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    result = {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PublicViewAuthResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, response.json())
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PublicViewTokenAuthResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: PublicViewAuthRequest,
) -> Response[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    """Returns a valid never-expiring JWT token for this public shared view if the password provided
    matches with the one saved by the view's owner.

    Args:
        slug (str):
        json_body (PublicViewAuthRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: PublicViewAuthRequest,
) -> Optional[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    """Returns a valid never-expiring JWT token for this public shared view if the password provided
    matches with the one saved by the view's owner.

    Args:
        slug (str):
        json_body (PublicViewAuthRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]
    """

    return sync_detailed(
        slug=slug,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: PublicViewAuthRequest,
) -> Response[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    """Returns a valid never-expiring JWT token for this public shared view if the password provided
    matches with the one saved by the view's owner.

    Args:
        slug (str):
        json_body (PublicViewAuthRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: PublicViewAuthRequest,
) -> Optional[Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]]:
    """Returns a valid never-expiring JWT token for this public shared view if the password provided
    matches with the one saved by the view's owner.

    Args:
        slug (str):
        json_body (PublicViewAuthRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PublicViewAuthResponse, PublicViewTokenAuthResponse404]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            json_body=json_body,
        )
    ).parsed
