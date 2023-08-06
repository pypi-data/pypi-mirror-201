from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_tables_response_400 import ListDatabaseTablesResponse400
from ...models.list_database_tables_response_404 import ListDatabaseTablesResponse404
from ...models.table import Table
from ...types import Response


def _get_kwargs(
    database_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/tables/database/{database_id}/".format(client.base_url, database_id=database_id)

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
) -> Optional[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Table.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTablesResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTablesResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    database_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    """Lists all the tables that are in the database related to the `database_id` parameter if the user has
    access to the database's workspace. A table is exactly as the name suggests. It can hold multiple
    fields, each having their own type and multiple rows. They can be added via the
    **create_database_table_field** and **create_database_table_row** endpoints.

    Args:
        database_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List['Table']]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    database_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    """Lists all the tables that are in the database related to the `database_id` parameter if the user has
    access to the database's workspace. A table is exactly as the name suggests. It can hold multiple
    fields, each having their own type and multiple rows. They can be added via the
    **create_database_table_field** and **create_database_table_row** endpoints.

    Args:
        database_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List['Table']]
    """

    return sync_detailed(
        database_id=database_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    database_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    """Lists all the tables that are in the database related to the `database_id` parameter if the user has
    access to the database's workspace. A table is exactly as the name suggests. It can hold multiple
    fields, each having their own type and multiple rows. They can be added via the
    **create_database_table_field** and **create_database_table_row** endpoints.

    Args:
        database_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List['Table']]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    database_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List["Table"]]]:
    """Lists all the tables that are in the database related to the `database_id` parameter if the user has
    access to the database's workspace. A table is exactly as the name suggests. It can hold multiple
    fields, each having their own type and multiple rows. They can be added via the
    **create_database_table_field** and **create_database_table_row** endpoints.

    Args:
        database_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTablesResponse400, ListDatabaseTablesResponse404, List['Table']]
    """

    return (
        await asyncio_detailed(
            database_id=database_id,
            client=client,
        )
    ).parsed
