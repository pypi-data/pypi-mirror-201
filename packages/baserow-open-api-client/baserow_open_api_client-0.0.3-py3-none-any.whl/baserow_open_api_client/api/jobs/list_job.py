from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.airtable_import_job_job import AirtableImportJobJob
from ...models.audit_log_export_job_job import AuditLogExportJobJob
from ...models.create_snapshot_job_job import CreateSnapshotJobJob
from ...models.duplicate_application_job_job import DuplicateApplicationJobJob
from ...models.duplicate_field_job_job import DuplicateFieldJobJob
from ...models.duplicate_page_job_job import DuplicatePageJobJob
from ...models.duplicate_table_job_job import DuplicateTableJobJob
from ...models.file_import_job_job import FileImportJobJob
from ...models.install_template_job_job import InstallTemplateJobJob
from ...models.restore_snapshot_job_job import RestoreSnapshotJobJob
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    job_ids: Union[Unset, None, str] = UNSET,
    states: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/jobs/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["job_ids"] = job_ids

    params["states"] = states

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
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> Union[
                "AirtableImportJobJob",
                "AuditLogExportJobJob",
                "CreateSnapshotJobJob",
                "DuplicateApplicationJobJob",
                "DuplicateFieldJobJob",
                "DuplicatePageJobJob",
                "DuplicateTableJobJob",
                "FileImportJobJob",
                "InstallTemplateJobJob",
                "RestoreSnapshotJobJob",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_0 = DuplicateApplicationJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_1 = InstallTemplateJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_2 = CreateSnapshotJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_3 = RestoreSnapshotJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_4 = AirtableImportJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_5 = FileImportJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_6 = DuplicateTableJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_7 = DuplicateFieldJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_job_type_job_type_8 = AuditLogExportJobJob.from_dict(data)

                    return componentsschemas_job_type_job_type_8
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_job_type_job_type_9 = DuplicatePageJobJob.from_dict(data)

                return componentsschemas_job_type_job_type_9

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    job_ids: Union[Unset, None, str] = UNSET,
    states: Union[Unset, None, str] = UNSET,
) -> Response[
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    """List all existing jobs. Jobs are task executed asynchronously in the background. You can use the
    `get_job` endpoint to read the currentprogress of a the job.

    Args:
        job_ids (Union[Unset, None, str]):
        states (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]]
    """

    kwargs = _get_kwargs(
        client=client,
        job_ids=job_ids,
        states=states,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    job_ids: Union[Unset, None, str] = UNSET,
    states: Union[Unset, None, str] = UNSET,
) -> Optional[
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    """List all existing jobs. Jobs are task executed asynchronously in the background. You can use the
    `get_job` endpoint to read the currentprogress of a the job.

    Args:
        job_ids (Union[Unset, None, str]):
        states (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]
    """

    return sync_detailed(
        client=client,
        job_ids=job_ids,
        states=states,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    job_ids: Union[Unset, None, str] = UNSET,
    states: Union[Unset, None, str] = UNSET,
) -> Response[
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    """List all existing jobs. Jobs are task executed asynchronously in the background. You can use the
    `get_job` endpoint to read the currentprogress of a the job.

    Args:
        job_ids (Union[Unset, None, str]):
        states (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]]
    """

    kwargs = _get_kwargs(
        client=client,
        job_ids=job_ids,
        states=states,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    job_ids: Union[Unset, None, str] = UNSET,
    states: Union[Unset, None, str] = UNSET,
) -> Optional[
    List[
        Union[
            "AirtableImportJobJob",
            "AuditLogExportJobJob",
            "CreateSnapshotJobJob",
            "DuplicateApplicationJobJob",
            "DuplicateFieldJobJob",
            "DuplicatePageJobJob",
            "DuplicateTableJobJob",
            "FileImportJobJob",
            "InstallTemplateJobJob",
            "RestoreSnapshotJobJob",
        ]
    ]
]:
    """List all existing jobs. Jobs are task executed asynchronously in the background. You can use the
    `get_job` endpoint to read the currentprogress of a the job.

    Args:
        job_ids (Union[Unset, None, str]):
        states (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]
    """

    return (
        await asyncio_detailed(
            client=client,
            job_ids=job_ids,
            states=states,
        )
    ).parsed
