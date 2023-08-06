from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_workspace_invitations_response_400 import ListWorkspaceInvitationsResponse400
from ...models.list_workspace_invitations_response_404 import ListWorkspaceInvitationsResponse404
from ...models.workspace_invitation import WorkspaceInvitation
from ...types import Response


def _get_kwargs(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/workspaces/invitations/workspace/{workspace_id}/".format(client.base_url, workspace_id=workspace_id)

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
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkspaceInvitation.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListWorkspaceInvitationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListWorkspaceInvitationsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    """Lists all the workspace invitations of the workspace related to the provided `workspace_id`
    parameter if the authorized user has admin rights to that workspace.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List['WorkspaceInvitation']]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    """Lists all the workspace invitations of the workspace related to the provided `workspace_id`
    parameter if the authorized user has admin rights to that workspace.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List['WorkspaceInvitation']]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    """Lists all the workspace invitations of the workspace related to the provided `workspace_id`
    parameter if the authorized user has admin rights to that workspace.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List['WorkspaceInvitation']]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List["WorkspaceInvitation"]]
]:
    """Lists all the workspace invitations of the workspace related to the provided `workspace_id`
    parameter if the authorized user has admin rights to that workspace.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListWorkspaceInvitationsResponse400, ListWorkspaceInvitationsResponse404, List['WorkspaceInvitation']]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
