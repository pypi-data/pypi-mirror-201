from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_table_rows_response_400 import ListDatabaseTableRowsResponse400
from ...models.list_database_table_rows_response_401 import ListDatabaseTableRowsResponse401
from ...models.list_database_table_rows_response_404 import ListDatabaseTableRowsResponse404
from ...models.pagination_serializer_example_row_response_serializer_with_user_field_names import (
    PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    exclude: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["exclude"] = exclude

    params["filter__{field}__{filter}"] = filter_field_filter

    params["filter_type"] = filter_type

    params["include"] = include

    params["order_by"] = order_by

    params["page"] = page

    params["search"] = search

    params["size"] = size

    params["user_field_names"] = user_field_names

    params["view_id"] = view_id

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
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerExampleRowResponseSerializerWithUserFieldNames.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListDatabaseTableRowsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    exclude: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Lists all the rows of the table related to the provided parameter if the user has access to the
    related database's workspace. The response is paginated by a page/size style. It is also possible to
    provide an optional search query, only rows where the data matches the search query are going to be
    returned then. The properties of the returned rows depends on which fields the table has. For a
    complete overview of fields use the **list_database_table_fields** endpoint to list them all. In the
    example all field types are listed, but normally the number in field_{id} key is going to be the id
    of the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name
    of the field. The value is what the user has provided and the format of it depends on the fields
    type.

    Args:
        table_id (int):
        exclude (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableRowsResponse400, ListDatabaseTableRowsResponse401, ListDatabaseTableRowsResponse404, PaginationSerializerExampleRowResponseSerializerWithUserFieldNames]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        exclude=exclude,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        order_by=order_by,
        page=page,
        search=search,
        size=size,
        user_field_names=user_field_names,
        view_id=view_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    table_id: int,
    *,
    client: AuthenticatedClient,
    exclude: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Lists all the rows of the table related to the provided parameter if the user has access to the
    related database's workspace. The response is paginated by a page/size style. It is also possible to
    provide an optional search query, only rows where the data matches the search query are going to be
    returned then. The properties of the returned rows depends on which fields the table has. For a
    complete overview of fields use the **list_database_table_fields** endpoint to list them all. In the
    example all field types are listed, but normally the number in field_{id} key is going to be the id
    of the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name
    of the field. The value is what the user has provided and the format of it depends on the fields
    type.

    Args:
        table_id (int):
        exclude (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableRowsResponse400, ListDatabaseTableRowsResponse401, ListDatabaseTableRowsResponse404, PaginationSerializerExampleRowResponseSerializerWithUserFieldNames]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        exclude=exclude,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        order_by=order_by,
        page=page,
        search=search,
        size=size,
        user_field_names=user_field_names,
        view_id=view_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    exclude: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Lists all the rows of the table related to the provided parameter if the user has access to the
    related database's workspace. The response is paginated by a page/size style. It is also possible to
    provide an optional search query, only rows where the data matches the search query are going to be
    returned then. The properties of the returned rows depends on which fields the table has. For a
    complete overview of fields use the **list_database_table_fields** endpoint to list them all. In the
    example all field types are listed, but normally the number in field_{id} key is going to be the id
    of the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name
    of the field. The value is what the user has provided and the format of it depends on the fields
    type.

    Args:
        table_id (int):
        exclude (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableRowsResponse400, ListDatabaseTableRowsResponse401, ListDatabaseTableRowsResponse404, PaginationSerializerExampleRowResponseSerializerWithUserFieldNames]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        exclude=exclude,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        order_by=order_by,
        page=page,
        search=search,
        size=size,
        user_field_names=user_field_names,
        view_id=view_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    exclude: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableRowsResponse400,
        ListDatabaseTableRowsResponse401,
        ListDatabaseTableRowsResponse404,
        PaginationSerializerExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Lists all the rows of the table related to the provided parameter if the user has access to the
    related database's workspace. The response is paginated by a page/size style. It is also possible to
    provide an optional search query, only rows where the data matches the search query are going to be
    returned then. The properties of the returned rows depends on which fields the table has. For a
    complete overview of fields use the **list_database_table_fields** endpoint to list them all. In the
    example all field types are listed, but normally the number in field_{id} key is going to be the id
    of the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name
    of the field. The value is what the user has provided and the format of it depends on the fields
    type.

    Args:
        table_id (int):
        exclude (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableRowsResponse400, ListDatabaseTableRowsResponse401, ListDatabaseTableRowsResponse404, PaginationSerializerExampleRowResponseSerializerWithUserFieldNames]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            exclude=exclude,
            filter_field_filter=filter_field_filter,
            filter_type=filter_type,
            include=include,
            order_by=order_by,
            page=page,
            search=search,
            size=size,
            user_field_names=user_field_names,
            view_id=view_id,
        )
    ).parsed
