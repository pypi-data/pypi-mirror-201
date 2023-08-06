from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_workspace import PatchedWorkspace
from ...models.update_group_response_400 import UpdateGroupResponse400
from ...models.update_group_response_404 import UpdateGroupResponse404
from ...models.workspace import Workspace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedWorkspace,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/groups/{group_id}/".format(client.base_url, group_id=group_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Workspace.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateGroupResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateGroupResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedWorkspace,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace](#tag/Workspaces/operation/update_workspace).**

    **Support for this endpoint will end in 2024.**

     Updates the existing group related to the provided `group_id` parameter if the authorized user
    belongs to the group. It is not yet possible to add additional users to a group.

    Args:
        group_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedWorkspace,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace](#tag/Workspaces/operation/update_workspace).**

    **Support for this endpoint will end in 2024.**

     Updates the existing group related to the provided `group_id` parameter if the authorized user
    belongs to the group. It is not yet possible to add additional users to a group.

    Args:
        group_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedWorkspace,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace](#tag/Workspaces/operation/update_workspace).**

    **Support for this endpoint will end in 2024.**

     Updates the existing group related to the provided `group_id` parameter if the authorized user
    belongs to the group. It is not yet possible to add additional users to a group.

    Args:
        group_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedWorkspace,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace](#tag/Workspaces/operation/update_workspace).**

    **Support for this endpoint will end in 2024.**

     Updates the existing group related to the provided `group_id` parameter if the authorized user
    belongs to the group. It is not yet possible to add additional users to a group.

    Args:
        group_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (PatchedWorkspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateGroupResponse400, UpdateGroupResponse404, Workspace]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
