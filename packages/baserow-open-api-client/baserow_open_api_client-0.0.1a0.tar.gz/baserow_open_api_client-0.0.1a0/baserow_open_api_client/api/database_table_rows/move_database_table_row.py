from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.example_row_response_serializer_with_user_field_names import (
    ExampleRowResponseSerializerWithUserFieldNames,
)
from ...models.move_database_table_row_response_400 import MoveDatabaseTableRowResponse400
from ...models.move_database_table_row_response_401 import MoveDatabaseTableRowResponse401
from ...models.move_database_table_row_response_404 import MoveDatabaseTableRowResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    before_id: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/{row_id}/move/".format(
        client.base_url, table_id=table_id, row_id=row_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    params: Dict[str, Any] = {}
    params["before_id"] = before_id

    params["user_field_names"] = user_field_names

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    result = {
        "method": "patch",
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
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExampleRowResponseSerializerWithUserFieldNames.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = MoveDatabaseTableRowResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = MoveDatabaseTableRowResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = MoveDatabaseTableRowResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
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
    before_id: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
    ]
]:
    """Moves the row related to given `row_id` parameter to another position. It is only possible to move
    the row before another existing row or to the end. If the `before_id` is provided then the row
    related to the `row_id` parameter is moved before that row. If the `before_id` parameter is not
    provided, then the row will be moved to the end.

    Args:
        table_id (int):
        row_id (int):
        before_id (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExampleRowResponseSerializerWithUserFieldNames, MoveDatabaseTableRowResponse400, MoveDatabaseTableRowResponse401, MoveDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        before_id=before_id,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    before_id: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
    ]
]:
    """Moves the row related to given `row_id` parameter to another position. It is only possible to move
    the row before another existing row or to the end. If the `before_id` is provided then the row
    related to the `row_id` parameter is moved before that row. If the `before_id` parameter is not
    provided, then the row will be moved to the end.

    Args:
        table_id (int):
        row_id (int):
        before_id (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExampleRowResponseSerializerWithUserFieldNames, MoveDatabaseTableRowResponse400, MoveDatabaseTableRowResponse401, MoveDatabaseTableRowResponse404]
    """

    return sync_detailed(
        table_id=table_id,
        row_id=row_id,
        client=client,
        before_id=before_id,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    before_id: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
    ]
]:
    """Moves the row related to given `row_id` parameter to another position. It is only possible to move
    the row before another existing row or to the end. If the `before_id` is provided then the row
    related to the `row_id` parameter is moved before that row. If the `before_id` parameter is not
    provided, then the row will be moved to the end.

    Args:
        table_id (int):
        row_id (int):
        before_id (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExampleRowResponseSerializerWithUserFieldNames, MoveDatabaseTableRowResponse400, MoveDatabaseTableRowResponse401, MoveDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        before_id=before_id,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    before_id: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        MoveDatabaseTableRowResponse400,
        MoveDatabaseTableRowResponse401,
        MoveDatabaseTableRowResponse404,
    ]
]:
    """Moves the row related to given `row_id` parameter to another position. It is only possible to move
    the row before another existing row or to the end. If the `before_id` is provided then the row
    related to the `row_id` parameter is moved before that row. If the `before_id` parameter is not
    provided, then the row will be moved to the end.

    Args:
        table_id (int):
        row_id (int):
        before_id (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExampleRowResponseSerializerWithUserFieldNames, MoveDatabaseTableRowResponse400, MoveDatabaseTableRowResponse401, MoveDatabaseTableRowResponse404]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            row_id=row_id,
            client=client,
            before_id=before_id,
            user_field_names=user_field_names,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
