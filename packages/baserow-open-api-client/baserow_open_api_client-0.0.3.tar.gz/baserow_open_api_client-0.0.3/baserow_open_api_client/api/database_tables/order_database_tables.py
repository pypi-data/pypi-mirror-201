from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_database_tables_response_400 import OrderDatabaseTablesResponse400
from ...models.order_database_tables_response_404 import OrderDatabaseTablesResponse404
from ...models.order_tables import OrderTables
from ...types import UNSET, Response, Unset


def _get_kwargs(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: OrderTables,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/tables/database/{database_id}/order/".format(client.base_url, database_id=database_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

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
) -> Optional[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = OrderDatabaseTablesResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = OrderDatabaseTablesResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
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
    json_body: OrderTables,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
    """Changes the order of the provided table ids to the matching position that the id has in the list. If
    the authorized user does not belong to the workspace it will be ignored. The order of the not
    provided tables will be set to `0`.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (OrderTables):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    json_body: OrderTables,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
    """Changes the order of the provided table ids to the matching position that the id has in the list. If
    the authorized user does not belong to the workspace it will be ignored. The order of the not
    provided tables will be set to `0`.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (OrderTables):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]
    """

    return sync_detailed(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: OrderTables,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
    """Changes the order of the provided table ids to the matching position that the id has in the list. If
    the authorized user does not belong to the workspace it will be ignored. The order of the not
    provided tables will be set to `0`.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (OrderTables):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: OrderTables,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]]:
    """Changes the order of the provided table ids to the matching position that the id has in the list. If
    the authorized user does not belong to the workspace it will be ignored. The order of the not
    provided tables will be set to `0`.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (OrderTables):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OrderDatabaseTablesResponse400, OrderDatabaseTablesResponse404]
    """

    return (
        await asyncio_detailed(
            database_id=database_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
