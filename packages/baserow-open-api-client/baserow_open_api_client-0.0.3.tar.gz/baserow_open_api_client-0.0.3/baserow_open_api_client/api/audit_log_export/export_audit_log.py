from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_audit_log_response_400 import ExportAuditLogResponse400
from ...models.single_audit_log_export_job_request import SingleAuditLogExportJobRequest
from ...models.single_audit_log_export_job_response import SingleAuditLogExportJobResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: SingleAuditLogExportJobRequest,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/admin/audit-log/export/".format(client.base_url)

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
) -> Optional[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleAuditLogExportJobResponse.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ExportAuditLogResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SingleAuditLogExportJobRequest,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    """Creates a job to export the filtered audit log to a CSV file.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (SingleAuditLogExportJobRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]
    """

    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    json_body: SingleAuditLogExportJobRequest,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    """Creates a job to export the filtered audit log to a CSV file.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (SingleAuditLogExportJobRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SingleAuditLogExportJobRequest,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    """Creates a job to export the filtered audit log to a CSV file.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (SingleAuditLogExportJobRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: SingleAuditLogExportJobRequest,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]]:
    """Creates a job to export the filtered audit log to a CSV file.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (SingleAuditLogExportJobRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExportAuditLogResponse400, SingleAuditLogExportJobResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
