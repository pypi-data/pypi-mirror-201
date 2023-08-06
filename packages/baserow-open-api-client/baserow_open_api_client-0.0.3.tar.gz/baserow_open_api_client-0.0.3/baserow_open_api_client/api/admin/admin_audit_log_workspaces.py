from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_audit_log_workspaces_response_400 import AdminAuditLogWorkspacesResponse400
from ...models.audit_log_workspace import AuditLogWorkspace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/admin/audit-log/workspaces/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["search"] = search

    params["size"] = size

    params["sorts"] = sorts

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
) -> Optional[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuditLogWorkspace.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminAuditLogWorkspacesResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Response[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    """List all distinct workspace names related to an audit log entry.

    Args:
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminAuditLogWorkspacesResponse400, Any, List['AuditLogWorkspace']]]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        search=search,
        size=size,
        sorts=sorts,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    """List all distinct workspace names related to an audit log entry.

    Args:
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminAuditLogWorkspacesResponse400, Any, List['AuditLogWorkspace']]
    """

    return sync_detailed(
        client=client,
        page=page,
        search=search,
        size=size,
        sorts=sorts,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Response[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    """List all distinct workspace names related to an audit log entry.

    Args:
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminAuditLogWorkspacesResponse400, Any, List['AuditLogWorkspace']]]
    """

    kwargs = _get_kwargs(
        client=client,
        page=page,
        search=search,
        size=size,
        sorts=sorts,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AdminAuditLogWorkspacesResponse400, Any, List["AuditLogWorkspace"]]]:
    """List all distinct workspace names related to an audit log entry.

    Args:
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminAuditLogWorkspacesResponse400, Any, List['AuditLogWorkspace']]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            search=search,
            size=size,
            sorts=sorts,
        )
    ).parsed
