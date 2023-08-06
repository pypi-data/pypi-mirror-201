from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.accept_workspace_invitation_response_400 import AcceptWorkspaceInvitationResponse400
from ...models.accept_workspace_invitation_response_404 import AcceptWorkspaceInvitationResponse404
from ...models.workspace_user_workspace import WorkspaceUserWorkspace
from ...types import Response


def _get_kwargs(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/workspaces/invitations/{workspace_invitation_id}/accept/".format(
        client.base_url, workspace_invitation_id=workspace_invitation_id
    )

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
) -> Optional[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceUserWorkspace.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AcceptWorkspaceInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AcceptWorkspaceInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    """Accepts a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]]
    """

    kwargs = _get_kwargs(
        workspace_invitation_id=workspace_invitation_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    """Accepts a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
    """

    return sync_detailed(
        workspace_invitation_id=workspace_invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    """Accepts a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]]
    """

    kwargs = _get_kwargs(
        workspace_invitation_id=workspace_invitation_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
]:
    """Accepts a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcceptWorkspaceInvitationResponse400, AcceptWorkspaceInvitationResponse404, WorkspaceUserWorkspace]
    """

    return (
        await asyncio_detailed(
            workspace_invitation_id=workspace_invitation_id,
            client=client,
        )
    ).parsed
