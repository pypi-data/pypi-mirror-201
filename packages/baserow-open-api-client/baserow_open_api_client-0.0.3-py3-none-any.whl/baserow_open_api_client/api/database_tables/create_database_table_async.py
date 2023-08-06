from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_table_async_response_400 import CreateDatabaseTableAsyncResponse400
from ...models.create_database_table_async_response_404 import CreateDatabaseTableAsyncResponse404
from ...models.single_file_import_job_serializer_class import SingleFileImportJobSerializerClass
from ...models.table_create import TableCreate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableCreate,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/tables/database/{database_id}/async/".format(client.base_url, database_id=database_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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
) -> Optional[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleFileImportJobSerializerClass.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableAsyncResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableAsyncResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
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
    json_body: TableCreate,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
    """Creates a job that creates a new table for the database related to the provided `database_id`
    parameter if the authorized user has access to the database's workspace. This endpoint is
    asynchronous and return the created job to track the progress of the task.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        json_body (TableCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
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
    json_body: TableCreate,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
    """Creates a job that creates a new table for the database related to the provided `database_id`
    parameter if the authorized user has access to the database's workspace. This endpoint is
    asynchronous and return the created job to track the progress of the task.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        json_body (TableCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
    """

    return sync_detailed(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableCreate,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
    """Creates a job that creates a new table for the database related to the provided `database_id`
    parameter if the authorized user has access to the database's workspace. This endpoint is
    asynchronous and return the created job to track the progress of the task.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        json_body (TableCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]]
    """

    kwargs = _get_kwargs(
        database_id=database_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    database_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableCreate,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
]:
    """Creates a job that creates a new table for the database related to the provided `database_id`
    parameter if the authorized user has access to the database's workspace. This endpoint is
    asynchronous and return the created job to track the progress of the task.

    Args:
        database_id (int):
        client_session_id (Union[Unset, str]):
        json_body (TableCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableAsyncResponse400, CreateDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
    """

    return (
        await asyncio_detailed(
            database_id=database_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
