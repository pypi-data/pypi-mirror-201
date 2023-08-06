from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.public_list_database_table_gallery_view_rows_response_400 import (
    PublicListDatabaseTableGalleryViewRowsResponse400,
)
from ...models.public_list_database_table_gallery_view_rows_response_401 import (
    PublicListDatabaseTableGalleryViewRowsResponse401,
)
from ...models.public_list_database_table_gallery_view_rows_response_404 import (
    PublicListDatabaseTableGalleryViewRowsResponse404,
)
from ...models.public_pagination_serializer_with_gallery_view_field_options_example_row_response import (
    PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/gallery/{slug}/public/rows/".format(client.base_url, slug=slug)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["count"] = count

    params["exclude_fields"] = exclude_fields

    params["filter__{field}__{filter}"] = filter_field_filter

    params["filter_type"] = filter_type

    params["include"] = include

    params["include_fields"] = include_fields

    params["limit"] = limit

    params["offset"] = offset

    params["order_by"] = order_by

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
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse.from_dict(
            response.json()
        )

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PublicListDatabaseTableGalleryViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = PublicListDatabaseTableGalleryViewRowsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PublicListDatabaseTableGalleryViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
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
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `slug` if the gallery view is
    public.The response is paginated either by a limit/offset or page/size style. The style depends on
    the provided GET parameters. The properties of the returned rows depends on which fields the table
    has. For a complete overview of fields use the **list_database_table_fields** endpoint to list them
    all. In the example all field types are listed, but normally the number in field_{id} key is going
    to be the id of the field. The value is what the user has provided and the format of it depends on
    the fields type.


    Args:
        slug (str):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PublicListDatabaseTableGalleryViewRowsResponse400, PublicListDatabaseTableGalleryViewRowsResponse401, PublicListDatabaseTableGalleryViewRowsResponse404, PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        order_by=order_by,
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
    slug: str,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `slug` if the gallery view is
    public.The response is paginated either by a limit/offset or page/size style. The style depends on
    the provided GET parameters. The properties of the returned rows depends on which fields the table
    has. For a complete overview of fields use the **list_database_table_fields** endpoint to list them
    all. In the example all field types are listed, but normally the number in field_{id} key is going
    to be the id of the field. The value is what the user has provided and the format of it depends on
    the fields type.


    Args:
        slug (str):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PublicListDatabaseTableGalleryViewRowsResponse400, PublicListDatabaseTableGalleryViewRowsResponse401, PublicListDatabaseTableGalleryViewRowsResponse404, PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]
    """

    return sync_detailed(
        slug=slug,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        order_by=order_by,
        page=page,
        search=search,
        size=size,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `slug` if the gallery view is
    public.The response is paginated either by a limit/offset or page/size style. The style depends on
    the provided GET parameters. The properties of the returned rows depends on which fields the table
    has. For a complete overview of fields use the **list_database_table_fields** endpoint to list them
    all. In the example all field types are listed, but normally the number in field_{id} key is going
    to be the id of the field. The value is what the user has provided and the format of it depends on
    the fields type.


    Args:
        slug (str):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PublicListDatabaseTableGalleryViewRowsResponse400, PublicListDatabaseTableGalleryViewRowsResponse401, PublicListDatabaseTableGalleryViewRowsResponse404, PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        count=count,
        exclude_fields=exclude_fields,
        filter_field_filter=filter_field_filter,
        filter_type=filter_type,
        include=include,
        include_fields=include_fields,
        limit=limit,
        offset=offset,
        order_by=order_by,
        page=page,
        search=search,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    count: Union[Unset, None, bool] = UNSET,
    exclude_fields: Union[Unset, None, str] = UNSET,
    filter_field_filter: Union[Unset, None, str] = UNSET,
    filter_type: Union[Unset, None, str] = UNSET,
    include: Union[Unset, None, str] = UNSET,
    include_fields: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        PublicListDatabaseTableGalleryViewRowsResponse400,
        PublicListDatabaseTableGalleryViewRowsResponse401,
        PublicListDatabaseTableGalleryViewRowsResponse404,
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse,
    ]
]:
    """Lists the requested rows of the view's table related to the provided `slug` if the gallery view is
    public.The response is paginated either by a limit/offset or page/size style. The style depends on
    the provided GET parameters. The properties of the returned rows depends on which fields the table
    has. For a complete overview of fields use the **list_database_table_fields** endpoint to list them
    all. In the example all field types are listed, but normally the number in field_{id} key is going
    to be the id of the field. The value is what the user has provided and the format of it depends on
    the fields type.


    Args:
        slug (str):
        count (Union[Unset, None, bool]):
        exclude_fields (Union[Unset, None, str]):
        filter_field_filter (Union[Unset, None, str]):
        filter_type (Union[Unset, None, str]):
        include (Union[Unset, None, str]):
        include_fields (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        order_by (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PublicListDatabaseTableGalleryViewRowsResponse400, PublicListDatabaseTableGalleryViewRowsResponse401, PublicListDatabaseTableGalleryViewRowsResponse404, PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            count=count,
            exclude_fields=exclude_fields,
            filter_field_filter=filter_field_filter,
            filter_type=filter_type,
            include=include,
            include_fields=include_fields,
            limit=limit,
            offset=offset,
            order_by=order_by,
            page=page,
            search=search,
            size=size,
        )
    ).parsed
