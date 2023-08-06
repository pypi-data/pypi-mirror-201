from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_undo_redo_request import PatchedUndoRedoRequest
from ...models.undo_redo_response import UndoRedoResponse
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PatchedUndoRedoRequest,
    client_session_id: str,
) -> Dict[str, Any]:
    url = "{}/api/user/undo/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["ClientSessionId"] = client_session_id

    json_json_body = json_body.to_dict()

    result = {
        "method": "patch",
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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[UndoRedoResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UndoRedoResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[UndoRedoResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PatchedUndoRedoRequest,
    client_session_id: str,
) -> Response[UndoRedoResponse]:
    """undoes the latest undoable action performed by the user making the request. a ClientSessionId header
    must be provided and only actions which were performed the same user with the same ClientSessionId
    value set on the api request that performed the action will be undone.Additionally the
    ClientSessionId header must be between 1 and 256 characters long and must only contain alphanumeric
    or the - characters.

    Args:
        client_session_id (str):
        json_body (PatchedUndoRedoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UndoRedoResponse]
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
    json_body: PatchedUndoRedoRequest,
    client_session_id: str,
) -> Optional[UndoRedoResponse]:
    """undoes the latest undoable action performed by the user making the request. a ClientSessionId header
    must be provided and only actions which were performed the same user with the same ClientSessionId
    value set on the api request that performed the action will be undone.Additionally the
    ClientSessionId header must be between 1 and 256 characters long and must only contain alphanumeric
    or the - characters.

    Args:
        client_session_id (str):
        json_body (PatchedUndoRedoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UndoRedoResponse
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PatchedUndoRedoRequest,
    client_session_id: str,
) -> Response[UndoRedoResponse]:
    """undoes the latest undoable action performed by the user making the request. a ClientSessionId header
    must be provided and only actions which were performed the same user with the same ClientSessionId
    value set on the api request that performed the action will be undone.Additionally the
    ClientSessionId header must be between 1 and 256 characters long and must only contain alphanumeric
    or the - characters.

    Args:
        client_session_id (str):
        json_body (PatchedUndoRedoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UndoRedoResponse]
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
    json_body: PatchedUndoRedoRequest,
    client_session_id: str,
) -> Optional[UndoRedoResponse]:
    """undoes the latest undoable action performed by the user making the request. a ClientSessionId header
    must be provided and only actions which were performed the same user with the same ClientSessionId
    value set on the api request that performed the action will be undone.Additionally the
    ClientSessionId header must be between 1 and 256 characters long and must only contain alphanumeric
    or the - characters.

    Args:
        client_session_id (str):
        json_body (PatchedUndoRedoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UndoRedoResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
