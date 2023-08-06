from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.airtable_import_job_job import AirtableImportJobJob
from ...models.audit_log_export_job_job import AuditLogExportJobJob
from ...models.create_job_response_400 import CreateJobResponse400
from ...models.create_job_response_404 import CreateJobResponse404
from ...models.create_snapshot_job_job import CreateSnapshotJobJob
from ...models.duplicate_application_job_job import DuplicateApplicationJobJob
from ...models.duplicate_field_job_job import DuplicateFieldJobJob
from ...models.duplicate_page_job_job import DuplicatePageJobJob
from ...models.duplicate_table_job_job import DuplicateTableJobJob
from ...models.file_import_job_job import FileImportJobJob
from ...models.install_template_job_job import InstallTemplateJobJob
from ...models.request_airtable_import_job_create_job import RequestAirtableImportJobCreateJob
from ...models.request_audit_log_export_job_create_job import RequestAuditLogExportJobCreateJob
from ...models.request_create_snapshot_job_create_job import RequestCreateSnapshotJobCreateJob
from ...models.request_duplicate_application_job_create_job import RequestDuplicateApplicationJobCreateJob
from ...models.request_duplicate_field_job_create_job import RequestDuplicateFieldJobCreateJob
from ...models.request_duplicate_page_job_create_job import RequestDuplicatePageJobCreateJob
from ...models.request_duplicate_table_job_create_job import RequestDuplicateTableJobCreateJob
from ...models.request_file_import_job_create_job import RequestFileImportJobCreateJob
from ...models.request_install_template_job_create_job import RequestInstallTemplateJobCreateJob
from ...models.request_restore_snapshot_job_create_job import RequestRestoreSnapshotJobCreateJob
from ...models.restore_snapshot_job_job import RestoreSnapshotJobJob
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestAirtableImportJobCreateJob",
        "RequestAuditLogExportJobCreateJob",
        "RequestCreateSnapshotJobCreateJob",
        "RequestDuplicateApplicationJobCreateJob",
        "RequestDuplicateFieldJobCreateJob",
        "RequestDuplicatePageJobCreateJob",
        "RequestDuplicateTableJobCreateJob",
        "RequestFileImportJobCreateJob",
        "RequestInstallTemplateJobCreateJob",
        "RequestRestoreSnapshotJobCreateJob",
    ],
) -> Dict[str, Any]:
    url = "{}/api/jobs/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body: Dict[str, Any]

    if isinstance(json_body, RequestDuplicateApplicationJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestInstallTemplateJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestCreateSnapshotJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestRestoreSnapshotJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestAirtableImportJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestFileImportJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestDuplicateTableJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestDuplicateFieldJobCreateJob):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestAuditLogExportJobCreateJob):
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
) -> Optional[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
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

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateJobResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateJobResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
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
    json_body: Union[
        "RequestAirtableImportJobCreateJob",
        "RequestAuditLogExportJobCreateJob",
        "RequestCreateSnapshotJobCreateJob",
        "RequestDuplicateApplicationJobCreateJob",
        "RequestDuplicateFieldJobCreateJob",
        "RequestDuplicatePageJobCreateJob",
        "RequestDuplicateTableJobCreateJob",
        "RequestFileImportJobCreateJob",
        "RequestInstallTemplateJobCreateJob",
        "RequestRestoreSnapshotJobCreateJob",
    ],
) -> Response[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
    ]
]:
    """Creates a new job. This job runs asynchronously in the background and execute the task specific to
    the provided typeparameters. The `get_job` can be used to get the current state of the job.

    Args:
        json_body (Union['RequestAirtableImportJobCreateJob', 'RequestAuditLogExportJobCreateJob',
            'RequestCreateSnapshotJobCreateJob', 'RequestDuplicateApplicationJobCreateJob',
            'RequestDuplicateFieldJobCreateJob', 'RequestDuplicatePageJobCreateJob',
            'RequestDuplicateTableJobCreateJob', 'RequestFileImportJobCreateJob',
            'RequestInstallTemplateJobCreateJob', 'RequestRestoreSnapshotJobCreateJob']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateJobResponse400, CreateJobResponse404, Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestAirtableImportJobCreateJob",
        "RequestAuditLogExportJobCreateJob",
        "RequestCreateSnapshotJobCreateJob",
        "RequestDuplicateApplicationJobCreateJob",
        "RequestDuplicateFieldJobCreateJob",
        "RequestDuplicatePageJobCreateJob",
        "RequestDuplicateTableJobCreateJob",
        "RequestFileImportJobCreateJob",
        "RequestInstallTemplateJobCreateJob",
        "RequestRestoreSnapshotJobCreateJob",
    ],
) -> Optional[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
    ]
]:
    """Creates a new job. This job runs asynchronously in the background and execute the task specific to
    the provided typeparameters. The `get_job` can be used to get the current state of the job.

    Args:
        json_body (Union['RequestAirtableImportJobCreateJob', 'RequestAuditLogExportJobCreateJob',
            'RequestCreateSnapshotJobCreateJob', 'RequestDuplicateApplicationJobCreateJob',
            'RequestDuplicateFieldJobCreateJob', 'RequestDuplicatePageJobCreateJob',
            'RequestDuplicateTableJobCreateJob', 'RequestFileImportJobCreateJob',
            'RequestInstallTemplateJobCreateJob', 'RequestRestoreSnapshotJobCreateJob']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateJobResponse400, CreateJobResponse404, Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestAirtableImportJobCreateJob",
        "RequestAuditLogExportJobCreateJob",
        "RequestCreateSnapshotJobCreateJob",
        "RequestDuplicateApplicationJobCreateJob",
        "RequestDuplicateFieldJobCreateJob",
        "RequestDuplicatePageJobCreateJob",
        "RequestDuplicateTableJobCreateJob",
        "RequestFileImportJobCreateJob",
        "RequestInstallTemplateJobCreateJob",
        "RequestRestoreSnapshotJobCreateJob",
    ],
) -> Response[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
    ]
]:
    """Creates a new job. This job runs asynchronously in the background and execute the task specific to
    the provided typeparameters. The `get_job` can be used to get the current state of the job.

    Args:
        json_body (Union['RequestAirtableImportJobCreateJob', 'RequestAuditLogExportJobCreateJob',
            'RequestCreateSnapshotJobCreateJob', 'RequestDuplicateApplicationJobCreateJob',
            'RequestDuplicateFieldJobCreateJob', 'RequestDuplicatePageJobCreateJob',
            'RequestDuplicateTableJobCreateJob', 'RequestFileImportJobCreateJob',
            'RequestInstallTemplateJobCreateJob', 'RequestRestoreSnapshotJobCreateJob']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateJobResponse400, CreateJobResponse404, Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestAirtableImportJobCreateJob",
        "RequestAuditLogExportJobCreateJob",
        "RequestCreateSnapshotJobCreateJob",
        "RequestDuplicateApplicationJobCreateJob",
        "RequestDuplicateFieldJobCreateJob",
        "RequestDuplicatePageJobCreateJob",
        "RequestDuplicateTableJobCreateJob",
        "RequestFileImportJobCreateJob",
        "RequestInstallTemplateJobCreateJob",
        "RequestRestoreSnapshotJobCreateJob",
    ],
) -> Optional[
    Union[
        CreateJobResponse400,
        CreateJobResponse404,
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
        ],
    ]
]:
    """Creates a new job. This job runs asynchronously in the background and execute the task specific to
    the provided typeparameters. The `get_job` can be used to get the current state of the job.

    Args:
        json_body (Union['RequestAirtableImportJobCreateJob', 'RequestAuditLogExportJobCreateJob',
            'RequestCreateSnapshotJobCreateJob', 'RequestDuplicateApplicationJobCreateJob',
            'RequestDuplicateFieldJobCreateJob', 'RequestDuplicatePageJobCreateJob',
            'RequestDuplicateTableJobCreateJob', 'RequestFileImportJobCreateJob',
            'RequestInstallTemplateJobCreateJob', 'RequestRestoreSnapshotJobCreateJob']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateJobResponse400, CreateJobResponse404, Union['AirtableImportJobJob', 'AuditLogExportJobJob', 'CreateSnapshotJobJob', 'DuplicateApplicationJobJob', 'DuplicateFieldJobJob', 'DuplicatePageJobJob', 'DuplicateTableJobJob', 'FileImportJobJob', 'InstallTemplateJobJob', 'RestoreSnapshotJobJob']]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
