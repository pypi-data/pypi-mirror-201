from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_list_role_assignments_response_400 import GroupListRoleAssignmentsResponse400
from ...models.group_list_role_assignments_response_404 import GroupListRoleAssignmentsResponse404
from ...models.open_api_role_assignment import OpenApiRoleAssignment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/role/{group_id}/".format(client.base_url, group_id=group_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["scope_id"] = scope_id

    params["scope_type"] = scope_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    result = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenApiRoleAssignment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GroupListRoleAssignmentsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GroupListRoleAssignmentsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
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
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_assign_role](#tag/Role-assignments/operation/workspace_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can list the role assignments within a group, optionally filtered down to a specific scope
    inside of that group. If the scope isn't specified,the group will be considered the scope.

    Args:
        group_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        scope_id=scope_id,
        scope_type=scope_type,
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
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_assign_role](#tag/Role-assignments/operation/workspace_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can list the role assignments within a group, optionally filtered down to a specific scope
    inside of that group. If the scope isn't specified,the group will be considered the scope.

    Args:
        group_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        scope_id=scope_id,
        scope_type=scope_type,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_assign_role](#tag/Role-assignments/operation/workspace_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can list the role assignments within a group, optionally filtered down to a specific scope
    inside of that group. If the scope isn't specified,the group will be considered the scope.

    Args:
        group_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        scope_id=scope_id,
        scope_type=scope_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_assign_role](#tag/Role-assignments/operation/workspace_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can list the role assignments within a group, optionally filtered down to a specific scope
    inside of that group. If the scope isn't specified,the group will be considered the scope.

    Args:
        group_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListRoleAssignmentsResponse400, GroupListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            scope_id=scope_id,
            scope_type=scope_type,
        )
    ).parsed
