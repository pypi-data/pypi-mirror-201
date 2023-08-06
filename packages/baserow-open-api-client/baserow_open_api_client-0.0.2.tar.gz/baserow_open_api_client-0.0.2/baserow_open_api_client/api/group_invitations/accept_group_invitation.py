from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.accept_group_invitation_response_400 import AcceptGroupInvitationResponse400
from ...models.accept_group_invitation_response_404 import AcceptGroupInvitationResponse404
from ...models.workspace_user_workspace import WorkspaceUserWorkspace
from ...types import Response


def _get_kwargs(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/groups/invitations/{group_invitation_id}/accept/".format(
        client.base_url, group_invitation_id=group_invitation_id
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
) -> Optional[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceUserWorkspace.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AcceptGroupInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AcceptGroupInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [accept_workspace_invitation](#tag/Workspace-invitations/operation/accept_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Accepts a group invitation with the given id if the email address of the user matches that of the
    invitation.

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]
    """

    kwargs = _get_kwargs(
        group_invitation_id=group_invitation_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [accept_workspace_invitation](#tag/Workspace-invitations/operation/accept_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Accepts a group invitation with the given id if the email address of the user matches that of the
    invitation.

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]
    """

    return sync_detailed(
        group_invitation_id=group_invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [accept_workspace_invitation](#tag/Workspace-invitations/operation/accept_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Accepts a group invitation with the given id if the email address of the user matches that of the
    invitation.

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]
    """

    kwargs = _get_kwargs(
        group_invitation_id=group_invitation_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [accept_workspace_invitation](#tag/Workspace-invitations/operation/accept_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Accepts a group invitation with the given id if the email address of the user matches that of the
    invitation.

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcceptGroupInvitationResponse400, AcceptGroupInvitationResponse404, WorkspaceUserWorkspace]
    """

    return (
        await asyncio_detailed(
            group_invitation_id=group_invitation_id,
            client=client,
        )
    ).parsed
