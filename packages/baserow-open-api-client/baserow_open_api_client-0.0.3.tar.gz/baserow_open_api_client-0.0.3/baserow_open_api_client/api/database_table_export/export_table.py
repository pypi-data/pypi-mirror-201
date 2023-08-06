from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_exporter_options import BaseExporterOptions
from ...models.csv_exporter_options import CsvExporterOptions
from ...models.export_job import ExportJob
from ...models.export_table_response_400 import ExportTableResponse400
from ...models.export_table_response_404 import ExportTableResponse404
from ...types import Response


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["BaseExporterOptions", "CsvExporterOptions"],
) -> Dict[str, Any]:
    url = "{}/api/database/export/table/{table_id}/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body: Dict[str, Any]

    if isinstance(json_body, CsvExporterOptions):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, BaseExporterOptions):
        json_json_body = json_body.to_dict()

    else:
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
) -> Optional[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExportJob.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ExportTableResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ExportTableResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
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
    json_body: Union["BaseExporterOptions", "CsvExporterOptions"],
) -> Response[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
    """Creates and starts a new export job for a table given some exporter options. Returns an error if the
    requesting user does not have permissionsto view the table.

    Args:
        table_id (int):
        json_body (Union['BaseExporterOptions', 'CsvExporterOptions']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]
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
    json_body: Union["BaseExporterOptions", "CsvExporterOptions"],
) -> Optional[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
    """Creates and starts a new export job for a table given some exporter options. Returns an error if the
    requesting user does not have permissionsto view the table.

    Args:
        table_id (int):
        json_body (Union['BaseExporterOptions', 'CsvExporterOptions']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportJob, ExportTableResponse400, ExportTableResponse404]
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
    json_body: Union["BaseExporterOptions", "CsvExporterOptions"],
) -> Response[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
    """Creates and starts a new export job for a table given some exporter options. Returns an error if the
    requesting user does not have permissionsto view the table.

    Args:
        table_id (int):
        json_body (Union['BaseExporterOptions', 'CsvExporterOptions']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]
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
    json_body: Union["BaseExporterOptions", "CsvExporterOptions"],
) -> Optional[Union[ExportJob, ExportTableResponse400, ExportTableResponse404]]:
    """Creates and starts a new export job for a table given some exporter options. Returns an error if the
    requesting user does not have permissionsto view the table.

    Args:
        table_id (int):
        json_body (Union['BaseExporterOptions', 'CsvExporterOptions']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportJob, ExportTableResponse400, ExportTableResponse404]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
