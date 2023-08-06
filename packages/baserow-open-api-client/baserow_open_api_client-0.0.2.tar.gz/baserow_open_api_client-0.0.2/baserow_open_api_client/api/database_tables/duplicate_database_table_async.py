from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_database_table_async_response_400 import DuplicateDatabaseTableAsyncResponse400
from ...models.duplicate_database_table_async_response_404 import DuplicateDatabaseTableAsyncResponse404
from ...models.single_duplicate_table_job_type import SingleDuplicateTableJobType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/tables/{table_id}/duplicate/async/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

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
) -> Optional[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleDuplicateTableJobType.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DuplicateDatabaseTableAsyncResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DuplicateDatabaseTableAsyncResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
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
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
]:
    """Start a job to duplicate the table with the provided `table_id` parameter if the authorized user has
    access to the database's workspace.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
]:
    """Start a job to duplicate the table with the provided `table_id` parameter if the authorized user has
    access to the database's workspace.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
]:
    """Start a job to duplicate the table with the provided `table_id` parameter if the authorized user has
    access to the database's workspace.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
]:
    """Start a job to duplicate the table with the provided `table_id` parameter if the authorized user has
    access to the database's workspace.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateDatabaseTableAsyncResponse400, DuplicateDatabaseTableAsyncResponse404, SingleDuplicateTableJobType]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
