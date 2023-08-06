from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_create_role_assignment import BatchCreateRoleAssignment
from ...models.group_batch_assign_role_response_400 import GroupBatchAssignRoleResponse400
from ...models.group_batch_assign_role_response_404 import GroupBatchAssignRoleResponse404
from ...models.open_api_role_assignment import OpenApiRoleAssignment
from ...types import Response


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: BatchCreateRoleAssignment,
) -> Dict[str, Any]:
    url = "{}/api/role/{group_id}/batch/".format(client.base_url, group_id=group_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    result = {
        "method": "post",
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
) -> Optional[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenApiRoleAssignment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GroupBatchAssignRoleResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GroupBatchAssignRoleResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
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
    json_body: BatchCreateRoleAssignment,
) -> Response[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_batch_assign_role](#tag/Role-assignments/operation/workspace_batch_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can assign a role to a multiple subjects into the given group for the given scope with this
    endpoint. If you want to remove the role you can omit the role property.

    Args:
        group_id (int):
        json_body (BatchCreateRoleAssignment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
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
    json_body: BatchCreateRoleAssignment,
) -> Optional[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_batch_assign_role](#tag/Role-assignments/operation/workspace_batch_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can assign a role to a multiple subjects into the given group for the given scope with this
    endpoint. If you want to remove the role you can omit the role property.

    Args:
        group_id (int):
        json_body (BatchCreateRoleAssignment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List['OpenApiRoleAssignment']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: BatchCreateRoleAssignment,
) -> Response[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_batch_assign_role](#tag/Role-assignments/operation/workspace_batch_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can assign a role to a multiple subjects into the given group for the given scope with this
    endpoint. If you want to remove the role you can omit the role property.

    Args:
        group_id (int):
        json_body (BatchCreateRoleAssignment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
    json_body: BatchCreateRoleAssignment,
) -> Optional[Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List["OpenApiRoleAssignment"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_batch_assign_role](#tag/Role-assignments/operation/workspace_batch_assign_role).**

    **Support for this endpoint will end in 2024.**

     You can assign a role to a multiple subjects into the given group for the given scope with this
    endpoint. If you want to remove the role you can omit the role property.

    Args:
        group_id (int):
        json_body (BatchCreateRoleAssignment):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupBatchAssignRoleResponse400, GroupBatchAssignRoleResponse404, List['OpenApiRoleAssignment']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
