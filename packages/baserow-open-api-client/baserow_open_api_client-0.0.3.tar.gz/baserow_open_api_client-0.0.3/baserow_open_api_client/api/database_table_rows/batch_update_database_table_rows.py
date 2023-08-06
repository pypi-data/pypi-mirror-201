from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_update_database_table_rows_response_400 import BatchUpdateDatabaseTableRowsResponse400
from ...models.batch_update_database_table_rows_response_401 import BatchUpdateDatabaseTableRowsResponse401
from ...models.batch_update_database_table_rows_response_404 import BatchUpdateDatabaseTableRowsResponse404
from ...models.example_batch_rows_response import ExampleBatchRowsResponse
from ...models.patched_example_batch_update_rows_request import PatchedExampleBatchUpdateRowsRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedExampleBatchUpdateRowsRequest,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/batch/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    params: Dict[str, Any] = {}
    params["user_field_names"] = user_field_names

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    result = {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExampleBatchRowsResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BatchUpdateDatabaseTableRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = BatchUpdateDatabaseTableRowsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BatchUpdateDatabaseTableRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
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
    json_body: PatchedExampleBatchUpdateRowsRequest,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
    ]
]:
    """Updates existing rows in the table if the user has access to the related table's workspace. The
    accepted body fields are depending on the fields that the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. None of the fields are
    required, if they are not provided the value is not going to be updated. When you want to update a
    value for the field with id `10`, the key must be named `field_10`. Or if the GET parameter
    `user_field_names` is provided the key of the field to update must be the name of the field.
    Multiple different fields to update can be provided for each row. In the examples below you will
    find all the different field types, the numbers/ids in the example are just there for example
    purposes, the field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

     **WARNING:** This endpoint doesn't yet work with row updated webhooks.

    Args:
        table_id (int):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedExampleBatchUpdateRowsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BatchUpdateDatabaseTableRowsResponse400, BatchUpdateDatabaseTableRowsResponse401, BatchUpdateDatabaseTableRowsResponse404, ExampleBatchRowsResponse]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
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
    *,
    client: AuthenticatedClient,
    json_body: PatchedExampleBatchUpdateRowsRequest,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
    ]
]:
    """Updates existing rows in the table if the user has access to the related table's workspace. The
    accepted body fields are depending on the fields that the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. None of the fields are
    required, if they are not provided the value is not going to be updated. When you want to update a
    value for the field with id `10`, the key must be named `field_10`. Or if the GET parameter
    `user_field_names` is provided the key of the field to update must be the name of the field.
    Multiple different fields to update can be provided for each row. In the examples below you will
    find all the different field types, the numbers/ids in the example are just there for example
    purposes, the field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

     **WARNING:** This endpoint doesn't yet work with row updated webhooks.

    Args:
        table_id (int):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedExampleBatchUpdateRowsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BatchUpdateDatabaseTableRowsResponse400, BatchUpdateDatabaseTableRowsResponse401, BatchUpdateDatabaseTableRowsResponse404, ExampleBatchRowsResponse]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedExampleBatchUpdateRowsRequest,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
    ]
]:
    """Updates existing rows in the table if the user has access to the related table's workspace. The
    accepted body fields are depending on the fields that the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. None of the fields are
    required, if they are not provided the value is not going to be updated. When you want to update a
    value for the field with id `10`, the key must be named `field_10`. Or if the GET parameter
    `user_field_names` is provided the key of the field to update must be the name of the field.
    Multiple different fields to update can be provided for each row. In the examples below you will
    find all the different field types, the numbers/ids in the example are just there for example
    purposes, the field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

     **WARNING:** This endpoint doesn't yet work with row updated webhooks.

    Args:
        table_id (int):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedExampleBatchUpdateRowsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BatchUpdateDatabaseTableRowsResponse400, BatchUpdateDatabaseTableRowsResponse401, BatchUpdateDatabaseTableRowsResponse404, ExampleBatchRowsResponse]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedExampleBatchUpdateRowsRequest,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        BatchUpdateDatabaseTableRowsResponse400,
        BatchUpdateDatabaseTableRowsResponse401,
        BatchUpdateDatabaseTableRowsResponse404,
        ExampleBatchRowsResponse,
    ]
]:
    """Updates existing rows in the table if the user has access to the related table's workspace. The
    accepted body fields are depending on the fields that the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. None of the fields are
    required, if they are not provided the value is not going to be updated. When you want to update a
    value for the field with id `10`, the key must be named `field_10`. Or if the GET parameter
    `user_field_names` is provided the key of the field to update must be the name of the field.
    Multiple different fields to update can be provided for each row. In the examples below you will
    find all the different field types, the numbers/ids in the example are just there for example
    purposes, the field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

     **WARNING:** This endpoint doesn't yet work with row updated webhooks.

    Args:
        table_id (int):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedExampleBatchUpdateRowsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BatchUpdateDatabaseTableRowsResponse400, BatchUpdateDatabaseTableRowsResponse401, BatchUpdateDatabaseTableRowsResponse404, ExampleBatchRowsResponse]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
            user_field_names=user_field_names,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
