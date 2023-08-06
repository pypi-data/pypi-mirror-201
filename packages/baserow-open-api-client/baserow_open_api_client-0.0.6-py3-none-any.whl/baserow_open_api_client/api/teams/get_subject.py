from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_subject_response_404 import GetSubjectResponse404
from ...models.team_subject_response import TeamSubjectResponse
from ...types import Response


def _get_kwargs(
    team_id: str,
    subject_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/teams/{team_id}/subjects/{subject_id}/".format(
        client.base_url, team_id=team_id, subject_id=subject_id
    )

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TeamSubjectResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetSubjectResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: str, subject_id: int, *, client: AuthenticatedClient, httpx_client=None
) -> Response[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    """Returns the information related to the provided subject id

    Args:
        team_id (str):
        subject_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSubjectResponse404, TeamSubjectResponse]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        subject_id=subject_id,
        client=client,
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
    team_id: str,
    subject_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    """Returns the information related to the provided subject id

    Args:
        team_id (str):
        subject_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSubjectResponse404, TeamSubjectResponse]
    """

    return sync_detailed(
        team_id=team_id,
        subject_id=subject_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    team_id: str,
    subject_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    """Returns the information related to the provided subject id

    Args:
        team_id (str):
        subject_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSubjectResponse404, TeamSubjectResponse]]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        subject_id=subject_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: str,
    subject_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetSubjectResponse404, TeamSubjectResponse]]:
    """Returns the information related to the provided subject id

    Args:
        team_id (str):
        subject_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSubjectResponse404, TeamSubjectResponse]
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            subject_id=subject_id,
            client=client,
        )
    ).parsed
