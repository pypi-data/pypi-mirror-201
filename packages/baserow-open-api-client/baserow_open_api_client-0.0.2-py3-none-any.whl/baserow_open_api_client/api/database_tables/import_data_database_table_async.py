from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.import_data_database_table_async_response_400 import ImportDataDatabaseTableAsyncResponse400
from ...models.import_data_database_table_async_response_404 import ImportDataDatabaseTableAsyncResponse404
from ...models.single_file_import_job_serializer_class import SingleFileImportJobSerializerClass
from ...models.table_import import TableImport
from ...types import Response


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableImport,
) -> Dict[str, Any]:
    url = "{}/api/database/tables/{table_id}/import/async/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
    ]
]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleFileImportJobSerializerClass.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ImportDataDatabaseTableAsyncResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ImportDataDatabaseTableAsyncResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
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
    json_body: TableImport,
) -> Response[
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
    ]
]:
    """Import data in the specified table if the authorized user has access to the related database's
    workspace. This endpoint is asynchronous and return the created job to track the progress of the
    task.

    Args:
        table_id (int):
        json_body (TableImport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ImportDataDatabaseTableAsyncResponse400, ImportDataDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
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
    json_body: TableImport,
) -> Optional[
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
    ]
]:
    """Import data in the specified table if the authorized user has access to the related database's
    workspace. This endpoint is asynchronous and return the created job to track the progress of the
    task.

    Args:
        table_id (int):
        json_body (TableImport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ImportDataDatabaseTableAsyncResponse400, ImportDataDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableImport,
) -> Response[
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
    ]
]:
    """Import data in the specified table if the authorized user has access to the related database's
    workspace. This endpoint is asynchronous and return the created job to track the progress of the
    task.

    Args:
        table_id (int):
        json_body (TableImport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ImportDataDatabaseTableAsyncResponse400, ImportDataDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TableImport,
) -> Optional[
    Union[
        ImportDataDatabaseTableAsyncResponse400,
        ImportDataDatabaseTableAsyncResponse404,
        SingleFileImportJobSerializerClass,
    ]
]:
    """Import data in the specified table if the authorized user has access to the related database's
    workspace. This endpoint is asynchronous and return the created job to track the progress of the
    task.

    Args:
        table_id (int):
        json_body (TableImport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ImportDataDatabaseTableAsyncResponse400, ImportDataDatabaseTableAsyncResponse404, SingleFileImportJobSerializerClass]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
