from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_database_token_response_400 import GetDatabaseTokenResponse400
from ...models.get_database_token_response_404 import GetDatabaseTokenResponse404
from ...models.token import Token
from ...types import Response


def _get_kwargs(
    token_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/tokens/{token_id}/".format(client.base_url, token_id=token_id)

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
) -> Optional[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Token.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetDatabaseTokenResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseTokenResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    """Returns the requested database token if it is owned by the authorized user andif the user has access
    to the related workspace.

    Args:
        token_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]
    """

    kwargs = _get_kwargs(
        token_id=token_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    """Returns the requested database token if it is owned by the authorized user andif the user has access
    to the related workspace.

    Args:
        token_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]
    """

    return sync_detailed(
        token_id=token_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    token_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    """Returns the requested database token if it is owned by the authorized user andif the user has access
    to the related workspace.

    Args:
        token_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]
    """

    kwargs = _get_kwargs(
        token_id=token_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]]:
    """Returns the requested database token if it is owned by the authorized user andif the user has access
    to the related workspace.

    Args:
        token_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTokenResponse400, GetDatabaseTokenResponse404, Token]
    """

    return (
        await asyncio_detailed(
            token_id=token_id,
            client=client,
        )
    ).parsed
