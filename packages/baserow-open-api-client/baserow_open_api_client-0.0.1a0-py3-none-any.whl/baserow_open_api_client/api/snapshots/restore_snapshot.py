from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job import Job
from ...models.restore_snapshot_response_400 import RestoreSnapshotResponse400
from ...models.restore_snapshot_response_404 import RestoreSnapshotResponse404
from ...types import Response


def _get_kwargs(
    snapshot_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/snapshots/{snapshot_id}/restore/".format(client.base_url, snapshot_id=snapshot_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Job.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RestoreSnapshotResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RestoreSnapshotResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    snapshot_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    """Restores a snapshot. When an application snapshot is restored, a new application will be created in
    the same workspace that the original application was placed in with the name of the snapshot and
    data that were in the original application at the time the snapshot was taken. The original
    application that the snapshot was taken from is unaffected. Snapshots can be restored multiple times
    and a number suffix is added to the new application name in the case of a collision.

    Args:
        snapshot_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]
    """

    kwargs = _get_kwargs(
        snapshot_id=snapshot_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    snapshot_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    """Restores a snapshot. When an application snapshot is restored, a new application will be created in
    the same workspace that the original application was placed in with the name of the snapshot and
    data that were in the original application at the time the snapshot was taken. The original
    application that the snapshot was taken from is unaffected. Snapshots can be restored multiple times
    and a number suffix is added to the new application name in the case of a collision.

    Args:
        snapshot_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]
    """

    return sync_detailed(
        snapshot_id=snapshot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    snapshot_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    """Restores a snapshot. When an application snapshot is restored, a new application will be created in
    the same workspace that the original application was placed in with the name of the snapshot and
    data that were in the original application at the time the snapshot was taken. The original
    application that the snapshot was taken from is unaffected. Snapshots can be restored multiple times
    and a number suffix is added to the new application name in the case of a collision.

    Args:
        snapshot_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]
    """

    kwargs = _get_kwargs(
        snapshot_id=snapshot_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    snapshot_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]]:
    """Restores a snapshot. When an application snapshot is restored, a new application will be created in
    the same workspace that the original application was placed in with the name of the snapshot and
    data that were in the original application at the time the snapshot was taken. The original
    application that the snapshot was taken from is unaffected. Snapshots can be restored multiple times
    and a number suffix is added to the new application name in the case of a collision.

    Args:
        snapshot_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Job, RestoreSnapshotResponse400, RestoreSnapshotResponse404]
    """

    return (
        await asyncio_detailed(
            snapshot_id=snapshot_id,
            client=client,
        )
    ).parsed
