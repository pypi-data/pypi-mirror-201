from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.workspace_user_workspace import WorkspaceUserWorkspace
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/workspaces/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[List["WorkspaceUserWorkspace"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkspaceUserWorkspace.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[List["WorkspaceUserWorkspace"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[List["WorkspaceUserWorkspace"]]:
    """Lists all the workspaces of the authorized user. A workspace can contain multiple applications like
    a database. Multiple users can have access to a workspace. For example each company could have their
    own workspace containing databases related to that company. The order of the workspaces are custom
    for each user. The order is configurable via the **order_workspaces** endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceUserWorkspace']]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[List["WorkspaceUserWorkspace"]]:
    """Lists all the workspaces of the authorized user. A workspace can contain multiple applications like
    a database. Multiple users can have access to a workspace. For example each company could have their
    own workspace containing databases related to that company. The order of the workspaces are custom
    for each user. The order is configurable via the **order_workspaces** endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceUserWorkspace']
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[List["WorkspaceUserWorkspace"]]:
    """Lists all the workspaces of the authorized user. A workspace can contain multiple applications like
    a database. Multiple users can have access to a workspace. For example each company could have their
    own workspace containing databases related to that company. The order of the workspaces are custom
    for each user. The order is configurable via the **order_workspaces** endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['WorkspaceUserWorkspace']]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[List["WorkspaceUserWorkspace"]]:
    """Lists all the workspaces of the authorized user. A workspace can contain multiple applications like
    a database. Multiple users can have access to a workspace. For example each company could have their
    own workspace containing databases related to that company. The order of the workspaces are custom
    for each user. The order is configurable via the **order_workspaces** endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['WorkspaceUserWorkspace']
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
