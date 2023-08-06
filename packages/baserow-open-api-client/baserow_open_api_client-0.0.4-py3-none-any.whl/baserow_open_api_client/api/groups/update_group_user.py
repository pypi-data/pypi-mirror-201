from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_update_workspace_user import PatchedUpdateWorkspaceUser
from ...models.update_group_user_response_400 import UpdateGroupUserResponse400
from ...models.update_group_user_response_404 import UpdateGroupUserResponse404
from ...models.workspace_user import WorkspaceUser
from ...types import Response


def _get_kwargs(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdateWorkspaceUser,
) -> Dict[str, Any]:
    url = "{}/api/groups/users/{group_user_id}/".format(client.base_url, group_user_id=group_user_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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
) -> Optional[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceUser.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateGroupUserResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateGroupUserResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_user_id: int, *, client: AuthenticatedClient, json_body: PatchedUpdateWorkspaceUser, httpx_client=None
) -> Response[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace_user](#tag/Workspaces/operation/update_workspace_user).**

     Updates the existing group user related to the provided `group_user_id` param if the authorized
    user has admin rights to the related group.

    Args:
        group_user_id (int):
        json_body (PatchedUpdateWorkspaceUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]
    """

    kwargs = _get_kwargs(
        group_user_id=group_user_id,
        client=client,
        json_body=json_body,
    )

    response = (httpx_client or httpx).request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdateWorkspaceUser,
) -> Optional[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace_user](#tag/Workspaces/operation/update_workspace_user).**

     Updates the existing group user related to the provided `group_user_id` param if the authorized
    user has admin rights to the related group.

    Args:
        group_user_id (int):
        json_body (PatchedUpdateWorkspaceUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]
    """

    return sync_detailed(
        group_user_id=group_user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdateWorkspaceUser,
) -> Response[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace_user](#tag/Workspaces/operation/update_workspace_user).**

     Updates the existing group user related to the provided `group_user_id` param if the authorized
    user has admin rights to the related group.

    Args:
        group_user_id (int):
        json_body (PatchedUpdateWorkspaceUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]
    """

    kwargs = _get_kwargs(
        group_user_id=group_user_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdateWorkspaceUser,
) -> Optional[Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [update_workspace_user](#tag/Workspaces/operation/update_workspace_user).**

     Updates the existing group user related to the provided `group_user_id` param if the authorized
    user has admin rights to the related group.

    Args:
        group_user_id (int):
        json_body (PatchedUpdateWorkspaceUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateGroupUserResponse400, UpdateGroupUserResponse404, WorkspaceUser]
    """

    return (
        await asyncio_detailed(
            group_user_id=group_user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
