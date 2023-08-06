from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_group_invitation_response_400 import CreateGroupInvitationResponse400
from ...models.create_group_invitation_response_404 import CreateGroupInvitationResponse404
from ...models.create_workspace_invitation import CreateWorkspaceInvitation
from ...models.workspace_invitation import WorkspaceInvitation
from ...types import Response


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreateWorkspaceInvitation,
) -> Dict[str, Any]:
    url = "{}/api/groups/invitations/group/{group_id}/".format(client.base_url, group_id=group_id)

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
) -> Optional[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceInvitation.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateGroupInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateGroupInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
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
    json_body: CreateWorkspaceInvitation,
) -> Response[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace_invitation](#tag/Workspace-invitations/operation/create_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Creates a new group invitations for an email address if the authorized user has admin rights to the
    related group. An email containing a sign up link will be send to the user.

    Args:
        group_id (int):
        json_body (CreateWorkspaceInvitation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
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
    json_body: CreateWorkspaceInvitation,
) -> Optional[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace_invitation](#tag/Workspace-invitations/operation/create_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Creates a new group invitations for an email address if the authorized user has admin rights to the
    related group. An email containing a sign up link will be send to the user.

    Args:
        group_id (int):
        json_body (CreateWorkspaceInvitation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreateWorkspaceInvitation,
) -> Response[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace_invitation](#tag/Workspace-invitations/operation/create_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Creates a new group invitations for an email address if the authorized user has admin rights to the
    related group. An email containing a sign up link will be send to the user.

    Args:
        group_id (int):
        json_body (CreateWorkspaceInvitation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreateWorkspaceInvitation,
) -> Optional[Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace_invitation](#tag/Workspace-invitations/operation/create_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Creates a new group invitations for an email address if the authorized user has admin rights to the
    related group. An email containing a sign up link will be send to the user.

    Args:
        group_id (int):
        json_body (CreateWorkspaceInvitation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateGroupInvitationResponse400, CreateGroupInvitationResponse404, WorkspaceInvitation]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
