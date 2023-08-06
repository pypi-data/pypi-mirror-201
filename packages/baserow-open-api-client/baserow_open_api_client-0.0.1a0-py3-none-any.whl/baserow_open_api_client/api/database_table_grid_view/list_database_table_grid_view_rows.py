from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_table_grid_view_rows_response_400 import ListDatabaseTableGridViewRowsResponse400
from ...models.list_database_table_grid_view_rows_response_404 import ListDatabaseTableGridViewRowsResponse404
from ...models.pagination_serializer_with_grid_view_field_options_example_row_response import (
    PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/grid/{view_id}/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["count"] = count

    params["exclude_fields"] = exclude_fields

    params["include"] = include

    params["include_fields"] = include_fields

    params["limit"] = limit

    params["offset"] = offset

    params["page"] = page

    params["search"] = search

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
) -> Optional[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerWithGridViewFieldOptionsExampleRowResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableGridViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableGridViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
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
    exclude_fields: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated either by a limit/offset or
    page/size style. The style depends on the provided GET parameters. The properties of the returned
    rows depends on which fields the table has. For a complete overview of fields use the
    **list_database_table_fields** endpoint to list them all. In the example all field types are listed,
    but normally the number in field_{id} key is going to be the id of the field. The value is what the
    user has provided and the format of it depends on the fields type.

    The filters and sortings are automatically applied. To get a full overview of the applied filters
    and sortings you can use the `list_database_table_view_filters` and
    `list_database_table_view_sortings` endpoints.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableGridViewRowsResponse400, ListDatabaseTableGridViewRowsResponse404, PaginationSerializerWithGridViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        page=page,
        search=search,
        size=size,
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
    exclude_fields: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated either by a limit/offset or
    page/size style. The style depends on the provided GET parameters. The properties of the returned
    rows depends on which fields the table has. For a complete overview of fields use the
    **list_database_table_fields** endpoint to list them all. In the example all field types are listed,
    but normally the number in field_{id} key is going to be the id of the field. The value is what the
    user has provided and the format of it depends on the fields type.

    The filters and sortings are automatically applied. To get a full overview of the applied filters
    and sortings you can use the `list_database_table_view_filters` and
    `list_database_table_view_sortings` endpoints.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableGridViewRowsResponse400, ListDatabaseTableGridViewRowsResponse404, PaginationSerializerWithGridViewFieldOptionsExampleRowResponse]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        page=page,
        search=search,
        size=size,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated either by a limit/offset or
    page/size style. The style depends on the provided GET parameters. The properties of the returned
    rows depends on which fields the table has. For a complete overview of fields use the
    **list_database_table_fields** endpoint to list them all. In the example all field types are listed,
    but normally the number in field_{id} key is going to be the id of the field. The value is what the
    user has provided and the format of it depends on the fields type.

    The filters and sortings are automatically applied. To get a full overview of the applied filters
    and sortings you can use the `list_database_table_view_filters` and
    `list_database_table_view_sortings` endpoints.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableGridViewRowsResponse400, ListDatabaseTableGridViewRowsResponse404, PaginationSerializerWithGridViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        page=page,
        search=search,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableGridViewRowsResponse400,
        ListDatabaseTableGridViewRowsResponse404,
        PaginationSerializerWithGridViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `view_id` if the authorized
    user has access to the database's workspace. The response is paginated either by a limit/offset or
    page/size style. The style depends on the provided GET parameters. The properties of the returned
    rows depends on which fields the table has. For a complete overview of fields use the
    **list_database_table_fields** endpoint to list them all. In the example all field types are listed,
    but normally the number in field_{id} key is going to be the id of the field. The value is what the
    user has provided and the format of it depends on the fields type.

    The filters and sortings are automatically applied. To get a full overview of the applied filters
    and sortings you can use the `list_database_table_view_filters` and
    `list_database_table_view_sortings` endpoints.

    Args:
        view_id (int):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableGridViewRowsResponse400, ListDatabaseTableGridViewRowsResponse404, PaginationSerializerWithGridViewFieldOptionsExampleRowResponse]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            count=count,
            exclude_fields=exclude_fields,
            include=include,
            include_fields=include_fields,
            limit=limit,
            offset=offset,
            page=page,
            search=search,
            size=size,
        )
    ).parsed
