from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_group_user_response_400 import DeleteGroupUserResponse400
from ...models.delete_group_user_response_404 import DeleteGroupUserResponse404
from ...types import Response


def _get_kwargs(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/groups/users/{group_user_id}/".format(client.base_url, group_user_id=group_user_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "delete",
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
) -> Optional[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DeleteGroupUserResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteGroupUserResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_user_id: int, *, client: AuthenticatedClient, httpx_client=None
) -> Response[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [delete_workspace_user](#tag/Workspaces/operation/delete_workspace_user).**

     Deletes a group user if the authorized user has admin rights to the related group.

    Args:
        group_user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]
    """

    kwargs = _get_kwargs(
        group_user_id=group_user_id,
        client=client,
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
) -> Optional[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [delete_workspace_user](#tag/Workspaces/operation/delete_workspace_user).**

     Deletes a group user if the authorized user has admin rights to the related group.

    Args:
        group_user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]
    """

    return sync_detailed(
        group_user_id=group_user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [delete_workspace_user](#tag/Workspaces/operation/delete_workspace_user).**

     Deletes a group user if the authorized user has admin rights to the related group.

    Args:
        group_user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]
    """

    kwargs = _get_kwargs(
        group_user_id=group_user_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_user_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [delete_workspace_user](#tag/Workspaces/operation/delete_workspace_user).**

     Deletes a group user if the authorized user has admin rights to the related group.

    Args:
        group_user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteGroupUserResponse400, DeleteGroupUserResponse404]
    """

    return (
        await asyncio_detailed(
            group_user_id=group_user_id,
            client=client,
        )
    ).parsed
