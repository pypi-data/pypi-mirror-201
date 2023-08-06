from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_group_invitation_response_400 import GetGroupInvitationResponse400
from ...models.get_group_invitation_response_404 import GetGroupInvitationResponse404
from ...models.workspace_invitation import WorkspaceInvitation
from ...types import Response


def _get_kwargs(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/groups/invitations/{group_invitation_id}/".format(
        client.base_url, group_invitation_id=group_invitation_id
    )

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
) -> Optional[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceInvitation.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetGroupInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetGroupInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
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
) -> Response[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation](#tag/Workspace-invitations/operation/get_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Returns the requested group invitation if the authorized user has admin right to the related group

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]
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
) -> Optional[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation](#tag/Workspace-invitations/operation/get_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Returns the requested group invitation if the authorized user has admin right to the related group

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]
    """

    return sync_detailed(
        group_invitation_id=group_invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_invitation_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation](#tag/Workspace-invitations/operation/get_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Returns the requested group invitation if the authorized user has admin right to the related group

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]
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
) -> Optional[Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation](#tag/Workspace-invitations/operation/get_workspace_invitation).**

    **Support for this endpoint will end in 2024.**

     Returns the requested group invitation if the authorized user has admin right to the related group

    Args:
        group_invitation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetGroupInvitationResponse400, GetGroupInvitationResponse404, WorkspaceInvitation]
    """

    return (
        await asyncio_detailed(
            group_invitation_id=group_invitation_id,
            client=client,
        )
    ).parsed
