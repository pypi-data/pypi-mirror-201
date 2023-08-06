from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_snapshots_response_400 import ListSnapshotsResponse400
from ...models.list_snapshots_response_404 import ListSnapshotsResponse404
from ...models.snapshot import Snapshot
from ...types import Response


def _get_kwargs(
    application_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/snapshots/application/{application_id}/".format(client.base_url, application_id=application_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "get",
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
) -> Optional[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Snapshot.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListSnapshotsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListSnapshotsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
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
) -> Response[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
    """Lists snapshots that were created for a given application.

    Args:
        application_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List['Snapshot']]]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        client=client,
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
) -> Optional[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
    """Lists snapshots that were created for a given application.

    Args:
        application_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List['Snapshot']]
    """

    return sync_detailed(
        application_id=application_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    application_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
    """Lists snapshots that were created for a given application.

    Args:
        application_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List['Snapshot']]]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List["Snapshot"]]]:
    """Lists snapshots that were created for a given application.

    Args:
        application_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListSnapshotsResponse400, ListSnapshotsResponse404, List['Snapshot']]
    """

    return (
        await asyncio_detailed(
            application_id=application_id,
            client=client,
        )
    ).parsed
