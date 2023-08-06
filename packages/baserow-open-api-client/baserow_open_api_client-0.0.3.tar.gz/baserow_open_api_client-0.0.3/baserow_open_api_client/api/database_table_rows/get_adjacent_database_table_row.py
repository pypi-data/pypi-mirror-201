from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.example_row_response_serializer_with_user_field_names import (
    ExampleRowResponseSerializerWithUserFieldNames,
)
from ...models.get_adjacent_database_table_row_response_400 import GetAdjacentDatabaseTableRowResponse400
from ...models.get_adjacent_database_table_row_response_404 import GetAdjacentDatabaseTableRowResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    previous: Union[Unset, None, bool] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/{row_id}/adjacent/".format(
        client.base_url, table_id=table_id, row_id=row_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["previous"] = previous

    params["search"] = search

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
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExampleRowResponseSerializerWithUserFieldNames.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetAdjacentDatabaseTableRowResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetAdjacentDatabaseTableRowResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
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
    row_id: int,
    *,
    client: AuthenticatedClient,
    previous: Union[Unset, None, bool] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
    ]
]:
    """Fetches the adjacent row to a given row_id in the table with the given table_id. If the previous
    flag is set it will return the previous row, otherwise it will return the next row. You can specifya
    view_id and it will apply the filters and sorts of the provided view.

    Args:
        table_id (int):
        row_id (int):
        previous (Union[Unset, None, bool]):
        search (Union[Unset, None, str]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ExampleRowResponseSerializerWithUserFieldNames, GetAdjacentDatabaseTableRowResponse400, GetAdjacentDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        previous=previous,
        search=search,
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
    row_id: int,
    *,
    client: AuthenticatedClient,
    previous: Union[Unset, None, bool] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
    ]
]:
    """Fetches the adjacent row to a given row_id in the table with the given table_id. If the previous
    flag is set it will return the previous row, otherwise it will return the next row. You can specifya
    view_id and it will apply the filters and sorts of the provided view.

    Args:
        table_id (int):
        row_id (int):
        previous (Union[Unset, None, bool]):
        search (Union[Unset, None, str]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ExampleRowResponseSerializerWithUserFieldNames, GetAdjacentDatabaseTableRowResponse400, GetAdjacentDatabaseTableRowResponse404]
    """

    return sync_detailed(
        table_id=table_id,
        row_id=row_id,
        client=client,
        previous=previous,
        search=search,
        user_field_names=user_field_names,
        view_id=view_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    previous: Union[Unset, None, bool] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Response[
    Union[
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
    ]
]:
    """Fetches the adjacent row to a given row_id in the table with the given table_id. If the previous
    flag is set it will return the previous row, otherwise it will return the next row. You can specifya
    view_id and it will apply the filters and sorts of the provided view.

    Args:
        table_id (int):
        row_id (int):
        previous (Union[Unset, None, bool]):
        search (Union[Unset, None, str]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ExampleRowResponseSerializerWithUserFieldNames, GetAdjacentDatabaseTableRowResponse400, GetAdjacentDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        previous=previous,
        search=search,
        user_field_names=user_field_names,
        view_id=view_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    previous: Union[Unset, None, bool] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    view_id: Union[Unset, None, int] = UNSET,
) -> Optional[
    Union[
        Any,
        ExampleRowResponseSerializerWithUserFieldNames,
        GetAdjacentDatabaseTableRowResponse400,
        GetAdjacentDatabaseTableRowResponse404,
    ]
]:
    """Fetches the adjacent row to a given row_id in the table with the given table_id. If the previous
    flag is set it will return the previous row, otherwise it will return the next row. You can specifya
    view_id and it will apply the filters and sorts of the provided view.

    Args:
        table_id (int):
        row_id (int):
        previous (Union[Unset, None, bool]):
        search (Union[Unset, None, str]):
        user_field_names (Union[Unset, None, bool]):
        view_id (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ExampleRowResponseSerializerWithUserFieldNames, GetAdjacentDatabaseTableRowResponse400, GetAdjacentDatabaseTableRowResponse404]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            row_id=row_id,
            client=client,
            previous=previous,
            search=search,
            user_field_names=user_field_names,
            view_id=view_id,
        )
    ).parsed
