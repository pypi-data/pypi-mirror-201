from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_table_gallery_view_rows_response_400 import ListDatabaseTableGalleryViewRowsResponse400
from ...models.list_database_table_gallery_view_rows_response_404 import ListDatabaseTableGalleryViewRowsResponse404
from ...models.pagination_serializer_with_gallery_view_field_options_example_row_response import (
    PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/gallery/{view_id}/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["count"] = count

    params["include"] = include

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

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
) -> Optional[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableGalleryViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableGalleryViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated by a limit/offset style.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableGalleryViewRowsResponse400, ListDatabaseTableGalleryViewRowsResponse404, PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        count=count,
        include=include,
        limit=limit,
        offset=offset,
        search=search,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated by a limit/offset style.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableGalleryViewRowsResponse400, ListDatabaseTableGalleryViewRowsResponse404, PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        count=count,
        include=include,
        limit=limit,
        offset=offset,
        search=search,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated by a limit/offset style.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableGalleryViewRowsResponse400, ListDatabaseTableGalleryViewRowsResponse404, PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        count=count,
        include=include,
        limit=limit,
        offset=offset,
        search=search,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableGalleryViewRowsResponse400,
        ListDatabaseTableGalleryViewRowsResponse404,
        PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated by a limit/offset style.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableGalleryViewRowsResponse400, ListDatabaseTableGalleryViewRowsResponse404, PaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            count=count,
            include=include,
            limit=limit,
            offset=offset,
            search=search,
        )
    ).parsed
