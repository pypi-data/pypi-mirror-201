from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.leave_workspace_response_400 import LeaveWorkspaceResponse400
from ...models.leave_workspace_response_404 import LeaveWorkspaceResponse404
from ...types import Response


def _get_kwargs(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/workspaces/{workspace_id}/leave/".format(client.base_url, workspace_id=workspace_id)

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
) -> Optional[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = LeaveWorkspaceResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = LeaveWorkspaceResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: int, *, client: AuthenticatedClient, httpx_client=None
) -> Response[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    """Makes the authenticated user leave the workspace related to the provided `workspace_id` if the user
    is in that workspace. If the user is the last admin in the workspace, he will not be able to leave
    it. There must always be one admin in the workspace, otherwise it will be left without control. If
    that is the case, he must either delete the workspace or give another member admin permissions
    first.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
    )

    response = (httpx_client or httpx).request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    """Makes the authenticated user leave the workspace related to the provided `workspace_id` if the user
    is in that workspace. If the user is the last admin in the workspace, he will not be able to leave
    it. There must always be one admin in the workspace, otherwise it will be left without control. If
    that is the case, he must either delete the workspace or give another member admin permissions
    first.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    """Makes the authenticated user leave the workspace related to the provided `workspace_id` if the user
    is in that workspace. If the user is the last admin in the workspace, he will not be able to leave
    it. There must always be one admin in the workspace, otherwise it will be left without control. If
    that is the case, he must either delete the workspace or give another member admin permissions
    first.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]
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
) -> Optional[Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]]:
    """Makes the authenticated user leave the workspace related to the provided `workspace_id` if the user
    is in that workspace. If the user is the last admin in the workspace, he will not be able to leave
    it. There must always be one admin in the workspace, otherwise it will be left without control. If
    that is the case, he must either delete the workspace or give another member admin permissions
    first.

    Args:
        workspace_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LeaveWorkspaceResponse400, LeaveWorkspaceResponse404]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
