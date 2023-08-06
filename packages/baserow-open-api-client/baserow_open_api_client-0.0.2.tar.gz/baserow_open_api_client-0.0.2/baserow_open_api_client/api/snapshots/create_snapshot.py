from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_snapshot_response_400 import CreateSnapshotResponse400
from ...models.create_snapshot_response_404 import CreateSnapshotResponse404
from ...models.job import Job
from ...models.snapshot import Snapshot
from ...types import Response


def _get_kwargs(
    application_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Snapshot,
) -> Dict[str, Any]:
    url = "{}/api/snapshots/application/{application_id}/".format(client.base_url, application_id=application_id)

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
) -> Optional[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = Job.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateSnapshotResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateSnapshotResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Snapshot,
) -> Response[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    """Creates a new application snapshot. Snapshots represent a state of an application at a specific
    point in time and can be restored later, making it easy to create backups of entire applications.

    Args:
        application_id (int):
        json_body (Snapshot):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Snapshot,
) -> Optional[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    """Creates a new application snapshot. Snapshots represent a state of an application at a specific
    point in time and can be restored later, making it easy to create backups of entire applications.

    Args:
        application_id (int):
        json_body (Snapshot):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]
    """

    return sync_detailed(
        application_id=application_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    application_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Snapshot,
) -> Response[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    """Creates a new application snapshot. Snapshots represent a state of an application at a specific
    point in time and can be restored later, making it easy to create backups of entire applications.

    Args:
        application_id (int):
        json_body (Snapshot):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Snapshot,
) -> Optional[Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]]:
    """Creates a new application snapshot. Snapshots represent a state of an application at a specific
    point in time and can be restored later, making it easy to create backups of entire applications.

    Args:
        application_id (int):
        json_body (Snapshot):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSnapshotResponse400, CreateSnapshotResponse404, Job]
    """

    return (
        await asyncio_detailed(
            application_id=application_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
