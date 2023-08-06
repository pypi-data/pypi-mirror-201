from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.team import Team
from ...models.team_response import TeamResponse
from ...models.update_team_response_400 import UpdateTeamResponse400
from ...models.update_team_response_404 import UpdateTeamResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Team,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/teams/{team_id}/".format(client.base_url, team_id=team_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    json_json_body = json_body.to_dict()

    result = {
        "method": "put",
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
) -> Optional[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TeamResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateTeamResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateTeamResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Team,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    """Updates an existing team with a new name.

    Args:
        team_id (str):
        client_session_id (Union[Unset, str]):
        json_body (Team): Mixin to a DRF serializer class to raise an exception if data with
            unknown fields
            is provided to the serializer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
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
    team_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Team,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    """Updates an existing team with a new name.

    Args:
        team_id (str):
        client_session_id (Union[Unset, str]):
        json_body (Team): Mixin to a DRF serializer class to raise an exception if data with
            unknown fields
            is provided to the serializer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Team,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    """Updates an existing team with a new name.

    Args:
        team_id (str):
        client_session_id (Union[Unset, str]):
        json_body (Team): Mixin to a DRF serializer class to raise an exception if data with
            unknown fields
            is provided to the serializer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    *,
    client: AuthenticatedClient,
    json_body: Team,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]]:
    """Updates an existing team with a new name.

    Args:
        team_id (str):
        client_session_id (Union[Unset, str]):
        json_body (Team): Mixin to a DRF serializer class to raise an exception if data with
            unknown fields
            is provided to the serializer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TeamResponse, UpdateTeamResponse400, UpdateTeamResponse404]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
