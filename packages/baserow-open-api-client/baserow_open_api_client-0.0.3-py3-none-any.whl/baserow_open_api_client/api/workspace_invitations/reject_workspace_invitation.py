from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reject_workspace_invitation_response_400 import RejectWorkspaceInvitationResponse400
from ...models.reject_workspace_invitation_response_404 import RejectWorkspaceInvitationResponse404
from ...types import Response


def _get_kwargs(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/workspaces/invitations/{workspace_invitation_id}/reject/".format(
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
) -> Optional[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RejectWorkspaceInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RejectWorkspaceInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
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
) -> Response[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
    """Rejects a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]
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
) -> Optional[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
    """Rejects a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]
    """

    return sync_detailed(
        workspace_invitation_id=workspace_invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
    """Rejects a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]
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
) -> Optional[Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]]:
    """Rejects a workspace invitation with the given id if the email address of the user matches that of
    the invitation.

    Args:
        workspace_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, RejectWorkspaceInvitationResponse400, RejectWorkspaceInvitationResponse404]
    """

    return (
        await asyncio_detailed(
            workspace_invitation_id=workspace_invitation_id,
            client=client,
        )
    ).parsed
