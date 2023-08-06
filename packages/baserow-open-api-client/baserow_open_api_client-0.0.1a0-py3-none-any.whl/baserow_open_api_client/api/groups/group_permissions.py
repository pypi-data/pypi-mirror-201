from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_permissions_response_404 import GroupPermissionsResponse404
from ...models.permission_object import PermissionObject
from ...types import Response


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/groups/{group_id}/permissions/".format(client.base_url, group_id=group_id)

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
) -> Optional[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PermissionObject.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GroupPermissionsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
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
) -> Response[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_permissions](#tag/Workspaces/operation/workspace_permissions).**

    **Support for this endpoint will end in 2024.**

     Returns a the permission data necessary to determine the permissions of a specific user over a
    specific group.
     See `core.handler.CoreHandler.get_permissions()` for more details.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupPermissionsResponse404, List['PermissionObject']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
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
) -> Optional[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_permissions](#tag/Workspaces/operation/workspace_permissions).**

    **Support for this endpoint will end in 2024.**

     Returns a the permission data necessary to determine the permissions of a specific user over a
    specific group.
     See `core.handler.CoreHandler.get_permissions()` for more details.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupPermissionsResponse404, List['PermissionObject']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_permissions](#tag/Workspaces/operation/workspace_permissions).**

    **Support for this endpoint will end in 2024.**

     Returns a the permission data necessary to determine the permissions of a specific user over a
    specific group.
     See `core.handler.CoreHandler.get_permissions()` for more details.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupPermissionsResponse404, List['PermissionObject']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GroupPermissionsResponse404, List["PermissionObject"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_permissions](#tag/Workspaces/operation/workspace_permissions).**

    **Support for this endpoint will end in 2024.**

     Returns a the permission data necessary to determine the permissions of a specific user over a
    specific group.
     See `core.handler.CoreHandler.get_permissions()` for more details.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupPermissionsResponse404, List['PermissionObject']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
        )
    ).parsed
