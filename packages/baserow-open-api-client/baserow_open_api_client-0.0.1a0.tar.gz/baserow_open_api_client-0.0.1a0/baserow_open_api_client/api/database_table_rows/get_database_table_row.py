from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.example_row_response_serializer_with_user_field_names import (
    ExampleRowResponseSerializerWithUserFieldNames,
)
from ...models.get_database_table_row_response_400 import GetDatabaseTableRowResponse400
from ...models.get_database_table_row_response_401 import GetDatabaseTableRowResponse401
from ...models.get_database_table_row_response_404 import GetDatabaseTableRowResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    user_field_names: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/table/{table_id}/{row_id}/".format(client.base_url, table_id=table_id, row_id=row_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["user_field_names"] = user_field_names

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
        ExampleRowResponseSerializerWithUserFieldNames,
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExampleRowResponseSerializerWithUserFieldNames.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetDatabaseTableRowResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetDatabaseTableRowResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseTableRowResponse404.from_dict(response.json())

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
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
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
    user_field_names: Union[Unset, None, bool] = UNSET,
) -> Response[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
    ]
]:
    """Fetches an existing row from the table if the user has access to the related table's workspace. The
    properties of the returned row depend on which fields the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. In the example all field
    types are listed, but normally the number in field_{id} key is going to be the id of the field of
    the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name of
    the field. The value is what the user has provided and the format of it depends on the fields type.

    Args:
        table_id (int):
        row_id (int):
        user_field_names (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExampleRowResponseSerializerWithUserFieldNames, GetDatabaseTableRowResponse400, GetDatabaseTableRowResponse401, GetDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        user_field_names=user_field_names,
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
    user_field_names: Union[Unset, None, bool] = UNSET,
) -> Optional[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
    ]
]:
    """Fetches an existing row from the table if the user has access to the related table's workspace. The
    properties of the returned row depend on which fields the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. In the example all field
    types are listed, but normally the number in field_{id} key is going to be the id of the field of
    the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name of
    the field. The value is what the user has provided and the format of it depends on the fields type.

    Args:
        table_id (int):
        row_id (int):
        user_field_names (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExampleRowResponseSerializerWithUserFieldNames, GetDatabaseTableRowResponse400, GetDatabaseTableRowResponse401, GetDatabaseTableRowResponse404]
    """

    return sync_detailed(
        table_id=table_id,
        row_id=row_id,
        client=client,
        user_field_names=user_field_names,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    user_field_names: Union[Unset, None, bool] = UNSET,
) -> Response[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
    ]
]:
    """Fetches an existing row from the table if the user has access to the related table's workspace. The
    properties of the returned row depend on which fields the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. In the example all field
    types are listed, but normally the number in field_{id} key is going to be the id of the field of
    the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name of
    the field. The value is what the user has provided and the format of it depends on the fields type.

    Args:
        table_id (int):
        row_id (int):
        user_field_names (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExampleRowResponseSerializerWithUserFieldNames, GetDatabaseTableRowResponse400, GetDatabaseTableRowResponse401, GetDatabaseTableRowResponse404]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        row_id=row_id,
        client=client,
        user_field_names=user_field_names,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    row_id: int,
    *,
    client: AuthenticatedClient,
    user_field_names: Union[Unset, None, bool] = UNSET,
) -> Optional[
    Union[
        ExampleRowResponseSerializerWithUserFieldNames,
        GetDatabaseTableRowResponse400,
        GetDatabaseTableRowResponse401,
        GetDatabaseTableRowResponse404,
    ]
]:
    """Fetches an existing row from the table if the user has access to the related table's workspace. The
    properties of the returned row depend on which fields the table has. For a complete overview of
    fields use the **list_database_table_fields** endpoint to list them all. In the example all field
    types are listed, but normally the number in field_{id} key is going to be the id of the field of
    the field. Or if the GET parameter `user_field_names` is provided then the keys will be the name of
    the field. The value is what the user has provided and the format of it depends on the fields type.

    Args:
        table_id (int):
        row_id (int):
        user_field_names (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExampleRowResponseSerializerWithUserFieldNames, GetDatabaseTableRowResponse400, GetDatabaseTableRowResponse401, GetDatabaseTableRowResponse404]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            row_id=row_id,
            client=client,
            user_field_names=user_field_names,
        )
    ).parsed
