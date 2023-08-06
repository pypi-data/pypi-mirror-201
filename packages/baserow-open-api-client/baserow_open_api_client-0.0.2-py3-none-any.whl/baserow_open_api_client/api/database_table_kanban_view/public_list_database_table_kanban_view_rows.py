from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.kanban_view_example_response import KanbanViewExampleResponse
from ...models.public_list_database_table_kanban_view_rows_response_400 import (
    PublicListDatabaseTableKanbanViewRowsResponse400,
)
from ...models.public_list_database_table_kanban_view_rows_response_401 import (
    PublicListDatabaseTableKanbanViewRowsResponse401,
)
from ...models.public_list_database_table_kanban_view_rows_response_404 import (
    PublicListDatabaseTableKanbanViewRowsResponse404,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    select_option: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/kanban/{slug}/public/rows/".format(client.base_url, slug=slug)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["offset"] = offset

    params["select_option"] = select_option

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
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = KanbanViewExampleResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = PublicListDatabaseTableKanbanViewRowsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PublicListDatabaseTableKanbanViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PublicListDatabaseTableKanbanViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
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
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    select_option: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by the view's single select field options related to the
    `slug` if the kanban view is publicly shared. Additional query parameters can be provided to control
    the `limit` and `offset` per select option.

    This is a **premium** feature.

    Args:
        slug (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        select_option (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[KanbanViewExampleResponse, PublicListDatabaseTableKanbanViewRowsResponse400, PublicListDatabaseTableKanbanViewRowsResponse401, PublicListDatabaseTableKanbanViewRowsResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        limit=limit,
        offset=offset,
        select_option=select_option,
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
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    select_option: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by the view's single select field options related to the
    `slug` if the kanban view is publicly shared. Additional query parameters can be provided to control
    the `limit` and `offset` per select option.

    This is a **premium** feature.

    Args:
        slug (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        select_option (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[KanbanViewExampleResponse, PublicListDatabaseTableKanbanViewRowsResponse400, PublicListDatabaseTableKanbanViewRowsResponse401, PublicListDatabaseTableKanbanViewRowsResponse404]
    """

    return sync_detailed(
        slug=slug,
        client=client,
        limit=limit,
        offset=offset,
        select_option=select_option,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    select_option: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by the view's single select field options related to the
    `slug` if the kanban view is publicly shared. Additional query parameters can be provided to control
    the `limit` and `offset` per select option.

    This is a **premium** feature.

    Args:
        slug (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        select_option (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[KanbanViewExampleResponse, PublicListDatabaseTableKanbanViewRowsResponse400, PublicListDatabaseTableKanbanViewRowsResponse401, PublicListDatabaseTableKanbanViewRowsResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        limit=limit,
        offset=offset,
        select_option=select_option,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    select_option: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        KanbanViewExampleResponse,
        PublicListDatabaseTableKanbanViewRowsResponse400,
        PublicListDatabaseTableKanbanViewRowsResponse401,
        PublicListDatabaseTableKanbanViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by the view's single select field options related to the
    `slug` if the kanban view is publicly shared. Additional query parameters can be provided to control
    the `limit` and `offset` per select option.

    This is a **premium** feature.

    Args:
        slug (str):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        select_option (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[KanbanViewExampleResponse, PublicListDatabaseTableKanbanViewRowsResponse400, PublicListDatabaseTableKanbanViewRowsResponse401, PublicListDatabaseTableKanbanViewRowsResponse404]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            limit=limit,
            offset=offset,
            select_option=select_option,
        )
    ).parsed
