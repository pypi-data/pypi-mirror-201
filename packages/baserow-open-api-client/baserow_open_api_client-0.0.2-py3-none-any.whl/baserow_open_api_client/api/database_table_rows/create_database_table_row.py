from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_table_row_response_400 import CreateDatabaseTableRowResponse400
from ...models.create_database_table_row_response_401 import CreateDatabaseTableRowResponse401
from ...models.create_database_table_row_response_404 import CreateDatabaseTableRowResponse404
from ...models.example_row_request_serializer_with_user_field_names import ExampleRowRequestSerializerWithUserFieldNames
from ...models.example_row_response_serializer_with_user_field_names import (
    ExampleRowResponseSerializerWithUserFieldNames,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequestSerializerWithUserFieldNames,
    before: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    params: Dict[str, Any] = {}
    params["before"] = before

    params["user_field_names"] = user_field_names

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    result = {
        "method": "post",
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
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExampleRowResponseSerializerWithUserFieldNames.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableRowResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreateDatabaseTableRowResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableRowResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
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
    json_body: ExampleRowRequestSerializerWithUserFieldNames,
    before: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Creates a new row in the table if the user has access to the related table's workspace. The accepted
    body fields are depending on the fields that the table has. For a complete overview of fields use
    the **list_database_table_fields** to list them all. None of the fields are required, if they are
    not provided the value is going to be `null` or `false` or some default value is that is set. If you
    want to add a value for the field with for example id `10`, the key must be named `field_10`. Or
    instead if the `user_field_names` GET param is provided the key must be the name of the field. Of
    course multiple fields can be provided in one request. In the examples below you will find all the
    different field types, the numbers/ids in the example are just there for example purposes, the
    field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

    Args:
        table_id (int):
        before (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ExampleRowRequestSerializerWithUserFieldNames):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableRowResponse400, CreateDatabaseTableRowResponse401, CreateDatabaseTableRowResponse404, ExampleRowResponseSerializerWithUserFieldNames]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        before=before,
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
    json_body: ExampleRowRequestSerializerWithUserFieldNames,
    before: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Creates a new row in the table if the user has access to the related table's workspace. The accepted
    body fields are depending on the fields that the table has. For a complete overview of fields use
    the **list_database_table_fields** to list them all. None of the fields are required, if they are
    not provided the value is going to be `null` or `false` or some default value is that is set. If you
    want to add a value for the field with for example id `10`, the key must be named `field_10`. Or
    instead if the `user_field_names` GET param is provided the key must be the name of the field. Of
    course multiple fields can be provided in one request. In the examples below you will find all the
    different field types, the numbers/ids in the example are just there for example purposes, the
    field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

    Args:
        table_id (int):
        before (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ExampleRowRequestSerializerWithUserFieldNames):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableRowResponse400, CreateDatabaseTableRowResponse401, CreateDatabaseTableRowResponse404, ExampleRowResponseSerializerWithUserFieldNames]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
        before=before,
        user_field_names=user_field_names,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequestSerializerWithUserFieldNames,
    before: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Creates a new row in the table if the user has access to the related table's workspace. The accepted
    body fields are depending on the fields that the table has. For a complete overview of fields use
    the **list_database_table_fields** to list them all. None of the fields are required, if they are
    not provided the value is going to be `null` or `false` or some default value is that is set. If you
    want to add a value for the field with for example id `10`, the key must be named `field_10`. Or
    instead if the `user_field_names` GET param is provided the key must be the name of the field. Of
    course multiple fields can be provided in one request. In the examples below you will find all the
    different field types, the numbers/ids in the example are just there for example purposes, the
    field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

    Args:
        table_id (int):
        before (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ExampleRowRequestSerializerWithUserFieldNames):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableRowResponse400, CreateDatabaseTableRowResponse401, CreateDatabaseTableRowResponse404, ExampleRowResponseSerializerWithUserFieldNames]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        before=before,
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
    json_body: ExampleRowRequestSerializerWithUserFieldNames,
    before: Union[Unset, None, int] = UNSET,
    user_field_names: Union[Unset, None, bool] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableRowResponse400,
        CreateDatabaseTableRowResponse401,
        CreateDatabaseTableRowResponse404,
        ExampleRowResponseSerializerWithUserFieldNames,
    ]
]:
    """Creates a new row in the table if the user has access to the related table's workspace. The accepted
    body fields are depending on the fields that the table has. For a complete overview of fields use
    the **list_database_table_fields** to list them all. None of the fields are required, if they are
    not provided the value is going to be `null` or `false` or some default value is that is set. If you
    want to add a value for the field with for example id `10`, the key must be named `field_10`. Or
    instead if the `user_field_names` GET param is provided the key must be the name of the field. Of
    course multiple fields can be provided in one request. In the examples below you will find all the
    different field types, the numbers/ids in the example are just there for example purposes, the
    field_ID must be replaced with the actual id of the field or the name of the field if
    `user_field_names` is provided.

    Args:
        table_id (int):
        before (Union[Unset, None, int]):
        user_field_names (Union[Unset, None, bool]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ExampleRowRequestSerializerWithUserFieldNames):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableRowResponse400, CreateDatabaseTableRowResponse401, CreateDatabaseTableRowResponse404, ExampleRowResponseSerializerWithUserFieldNames]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
            before=before,
            user_field_names=user_field_names,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
