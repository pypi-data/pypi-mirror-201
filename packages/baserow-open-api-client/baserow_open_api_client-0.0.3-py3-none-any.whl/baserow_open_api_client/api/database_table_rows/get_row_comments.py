from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_row_comments_response_400 import GetRowCommentsResponse400
from ...models.get_row_comments_response_404 import GetRowCommentsResponse404
from ...models.pagination_serializer_row_comment import PaginationSerializerRowComment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/row_comments/{table_id}/{row_id}/".format(client.base_url, table_id=table_id, row_id=row_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["offset"] = offset

    params["page"] = page

    params["size"] = size

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
) -> Optional[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerRowComment.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetRowCommentsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetRowCommentsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    """Returns all row comments for the specified table and row.

    Args:
        table_id (int):
        row_id (int):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        limit=limit,
        offset=offset,
        page=page,
        size=size,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    """Returns all row comments for the specified table and row.

    Args:
        table_id (int):
        row_id (int):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]
    """

    return sync_detailed(
        table_id=table_id,
        row_id=row_id,
        client=client,
        limit=limit,
        offset=offset,
        page=page,
        size=size,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    """Returns all row comments for the specified table and row.

    Args:
        table_id (int):
        row_id (int):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        limit=limit,
        offset=offset,
        page=page,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]]:
    """Returns all row comments for the specified table and row.

    Args:
        table_id (int):
        row_id (int):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetRowCommentsResponse400, GetRowCommentsResponse404, PaginationSerializerRowComment]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            row_id=row_id,
            client=client,
            limit=limit,
            offset=offset,
            page=page,
            size=size,
        )
    ).parsed
