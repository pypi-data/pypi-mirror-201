from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.workspace import Workspace
from ...models.workspace_user_workspace import WorkspaceUserWorkspace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/groups/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[WorkspaceUserWorkspace]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkspaceUserWorkspace.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[WorkspaceUserWorkspace]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[WorkspaceUserWorkspace]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace](#tag/Workspaces/operation/create_workspace).**

    **Support for this endpoint will end in 2024.**

     Creates a new group where only the authorized user has access to. No initial data like database
    applications are added, they have to be created via other endpoints.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (Workspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceUserWorkspace]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[WorkspaceUserWorkspace]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace](#tag/Workspaces/operation/create_workspace).**

    **Support for this endpoint will end in 2024.**

     Creates a new group where only the authorized user has access to. No initial data like database
    applications are added, they have to be created via other endpoints.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (Workspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceUserWorkspace
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[WorkspaceUserWorkspace]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace](#tag/Workspaces/operation/create_workspace).**

    **Support for this endpoint will end in 2024.**

     Creates a new group where only the authorized user has access to. No initial data like database
    applications are added, they have to be created via other endpoints.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (Workspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkspaceUserWorkspace]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: Workspace,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[WorkspaceUserWorkspace]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [create_workspace](#tag/Workspaces/operation/create_workspace).**

    **Support for this endpoint will end in 2024.**

     Creates a new group where only the authorized user has access to. No initial data like database
    applications are added, they have to be created via other endpoints.

    Args:
        client_session_id (Union[Unset, str]):
        json_body (Workspace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkspaceUserWorkspace
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
