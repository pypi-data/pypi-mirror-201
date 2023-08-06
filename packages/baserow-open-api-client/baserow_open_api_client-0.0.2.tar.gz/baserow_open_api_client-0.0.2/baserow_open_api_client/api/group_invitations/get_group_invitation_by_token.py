from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_group_invitation_by_token_response_400 import GetGroupInvitationByTokenResponse400
from ...models.get_group_invitation_by_token_response_404 import GetGroupInvitationByTokenResponse404
from ...models.user_workspace_invitation import UserWorkspaceInvitation
from ...types import Response


def _get_kwargs(
    token: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/groups/invitations/token/{token}/".format(client.base_url, token=token)

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
) -> Optional[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserWorkspaceInvitation.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetGroupInvitationByTokenResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetGroupInvitationByTokenResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation_by_token](#tag/Workspace-
    invitations/operation/get_workspace_invitation_by_token).**

    **Support for this endpoint will end in 2024.**

     Responds with the serialized group invitation if an invitation with the provided token is found.

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]]
    """

    kwargs = _get_kwargs(
        token=token,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation_by_token](#tag/Workspace-
    invitations/operation/get_workspace_invitation_by_token).**

    **Support for this endpoint will end in 2024.**

     Responds with the serialized group invitation if an invitation with the provided token is found.

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
    """

    return sync_detailed(
        token=token,
        client=client,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation_by_token](#tag/Workspace-
    invitations/operation/get_workspace_invitation_by_token).**

    **Support for this endpoint will end in 2024.**

     Responds with the serialized group invitation if an invitation with the provided token is found.

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]]
    """

    kwargs = _get_kwargs(
        token=token,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [get_workspace_invitation_by_token](#tag/Workspace-
    invitations/operation/get_workspace_invitation_by_token).**

    **Support for this endpoint will end in 2024.**

     Responds with the serialized group invitation if an invitation with the provided token is found.

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetGroupInvitationByTokenResponse400, GetGroupInvitationByTokenResponse404, UserWorkspaceInvitation]
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
        )
    ).parsed
