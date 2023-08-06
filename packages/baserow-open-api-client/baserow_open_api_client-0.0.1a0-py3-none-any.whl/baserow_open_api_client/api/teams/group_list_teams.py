from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_list_teams_response_404 import GroupListTeamsResponse404
from ...models.team_response import TeamResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
    search: Union[Unset, None, str] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/teams/group/{group_id}/".format(client.base_url, group_id=group_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["search"] = search

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
) -> Optional[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TeamResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GroupListTeamsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
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
    search: Union[Unset, None, str] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Response[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_teams](#tag/Teams/operation/workspace_list_teams).**

    **Support for this endpoint will end in 2024.**

     Lists all teams in a given group.

    Args:
        group_id (int):
        search (Union[Unset, None, str]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListTeamsResponse404, List['TeamResponse']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        search=search,
        sorts=sorts,
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
    search: Union[Unset, None, str] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Optional[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_teams](#tag/Teams/operation/workspace_list_teams).**

    **Support for this endpoint will end in 2024.**

     Lists all teams in a given group.

    Args:
        group_id (int):
        search (Union[Unset, None, str]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListTeamsResponse404, List['TeamResponse']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        search=search,
        sorts=sorts,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
    search: Union[Unset, None, str] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Response[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_teams](#tag/Teams/operation/workspace_list_teams).**

    **Support for this endpoint will end in 2024.**

     Lists all teams in a given group.

    Args:
        group_id (int):
        search (Union[Unset, None, str]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListTeamsResponse404, List['TeamResponse']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
        search=search,
        sorts=sorts,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
    search: Union[Unset, None, str] = UNSET,
    sorts: Union[Unset, None, str] = UNSET,
) -> Optional[Union[GroupListTeamsResponse404, List["TeamResponse"]]]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_teams](#tag/Teams/operation/workspace_list_teams).**

    **Support for this endpoint will end in 2024.**

     Lists all teams in a given group.

    Args:
        group_id (int):
        search (Union[Unset, None, str]):
        sorts (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListTeamsResponse404, List['TeamResponse']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            search=search,
            sorts=sorts,
        )
    ).parsed
