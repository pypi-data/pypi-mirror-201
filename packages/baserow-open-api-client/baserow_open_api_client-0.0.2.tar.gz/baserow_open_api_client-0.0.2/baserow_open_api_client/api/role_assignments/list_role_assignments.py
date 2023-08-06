from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_role_assignments_response_400 import ListRoleAssignmentsResponse400
from ...models.list_role_assignments_response_404 import ListRoleAssignmentsResponse404
from ...models.open_api_role_assignment import OpenApiRoleAssignment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/role/{workspace_id}/".format(client.base_url, workspace_id=workspace_id)

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
) -> Optional[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenApiRoleAssignment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListRoleAssignmentsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListRoleAssignmentsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
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
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Response[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
    """You can list the role assignments within a workspace, optionally filtered downto a specific scope
    inside of that workspace. If the scope isn't specified,the workspace will be considered the scope.

    Args:
        workspace_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
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
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
    """You can list the role assignments within a workspace, optionally filtered downto a specific scope
    inside of that workspace. If the scope isn't specified,the workspace will be considered the scope.

    Args:
        workspace_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        scope_id=scope_id,
        scope_type=scope_type,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Response[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
    """You can list the role assignments within a workspace, optionally filtered downto a specific scope
    inside of that workspace. If the scope isn't specified,the workspace will be considered the scope.

    Args:
        workspace_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
        scope_id=scope_id,
        scope_type=scope_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    scope_id: Union[Unset, None, int] = UNSET,
    scope_type: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List["OpenApiRoleAssignment"]]]:
    """You can list the role assignments within a workspace, optionally filtered downto a specific scope
    inside of that workspace. If the scope isn't specified,the workspace will be considered the scope.

    Args:
        workspace_id (int):
        scope_id (Union[Unset, None, int]):
        scope_type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListRoleAssignmentsResponse400, ListRoleAssignmentsResponse404, List['OpenApiRoleAssignment']]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            scope_id=scope_id,
            scope_type=scope_type,
        )
    ).parsed
