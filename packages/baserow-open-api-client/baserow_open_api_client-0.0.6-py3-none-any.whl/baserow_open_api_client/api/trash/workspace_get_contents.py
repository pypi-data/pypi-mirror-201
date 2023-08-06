from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pagination_serializer_trash_contents import PaginationSerializerTrashContents
from ...models.workspace_get_contents_response_400 import WorkspaceGetContentsResponse400
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    application_id: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/trash/workspace/{workspace_id}/".format(client.base_url, workspace_id=workspace_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["application_id"] = application_id

    params["page"] = page

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
) -> Optional[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerTrashContents.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = WorkspaceGetContentsResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
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
    application_id: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    httpx_client=None,
) -> Response[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
    """Responds with trash contents for a workspace optionally filtered to a specific application.

    Args:
        workspace_id (int):
        application_id (Union[Unset, None, int]):
        page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
        application_id=application_id,
        page=page,
    )

    if httpx_client:
        response = httpx_client.request(
            **kwargs,
        )
    else:
        response = httpx.request(
            verify=client.verify_ssl,
            **kwargs,
        )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    application_id: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
) -> Optional[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
    """Responds with trash contents for a workspace optionally filtered to a specific application.

    Args:
        workspace_id (int):
        application_id (Union[Unset, None, int]):
        page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        application_id=application_id,
        page=page,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    application_id: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
) -> Response[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
    """Responds with trash contents for a workspace optionally filtered to a specific application.

    Args:
        workspace_id (int):
        application_id (Union[Unset, None, int]):
        page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
        application_id=application_id,
        page=page,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    application_id: Union[Unset, None, int] = UNSET,
    page: Union[Unset, None, int] = UNSET,
) -> Optional[Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]]:
    """Responds with trash contents for a workspace optionally filtered to a specific application.

    Args:
        workspace_id (int):
        application_id (Union[Unset, None, int]):
        page (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PaginationSerializerTrashContents, WorkspaceGetContentsResponse400]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            application_id=application_id,
            page=page,
        )
    ).parsed
