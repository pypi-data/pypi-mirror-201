from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_public_view_info_response_400 import GetPublicViewInfoResponse400
from ...models.get_public_view_info_response_401 import GetPublicViewInfoResponse401
from ...models.get_public_view_info_response_404 import GetPublicViewInfoResponse404
from ...models.public_view_info import PublicViewInfo
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{slug}/public/info/".format(client.base_url, slug=slug)

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
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PublicViewInfo.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetPublicViewInfoResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetPublicViewInfoResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetPublicViewInfoResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str, *, client: AuthenticatedClient, httpx_client=None
) -> Response[
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    """Returns the required public information to display a single shared view.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
    )

    if httpx_client:
        response = httpx_client.request(
            **kwargs,
        )
    else:
        response = httpx.request(
            verify=client.verify_ssl,
            **kwargs,
        )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    """Returns the required public information to display a single shared view.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
    """

    return sync_detailed(
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    """Returns the required public information to display a single shared view.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
]:
    """Returns the required public information to display a single shared view.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPublicViewInfoResponse400, GetPublicViewInfoResponse401, GetPublicViewInfoResponse404, PublicViewInfo]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
        )
    ).parsed
