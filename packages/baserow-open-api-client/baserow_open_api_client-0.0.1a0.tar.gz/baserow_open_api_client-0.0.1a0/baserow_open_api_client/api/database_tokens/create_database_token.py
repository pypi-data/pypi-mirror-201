from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_token_response_400 import CreateDatabaseTokenResponse400
from ...models.token import Token
from ...models.token_create import TokenCreate
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: TokenCreate,
) -> Dict[str, Any]:
    url = "{}/api/database/tokens/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[CreateDatabaseTokenResponse400, Token]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Token.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTokenResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateDatabaseTokenResponse400, Token]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: TokenCreate,
) -> Response[Union[CreateDatabaseTokenResponse400, Token]]:
    """Creates a new database token for a given workspace and for the authorized user.

    Args:
        json_body (TokenCreate): A mixin that allows us to rename the `group` field to `workspace`
            when serializing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTokenResponse400, Token]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: TokenCreate,
) -> Optional[Union[CreateDatabaseTokenResponse400, Token]]:
    """Creates a new database token for a given workspace and for the authorized user.

    Args:
        json_body (TokenCreate): A mixin that allows us to rename the `group` field to `workspace`
            when serializing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTokenResponse400, Token]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: TokenCreate,
) -> Response[Union[CreateDatabaseTokenResponse400, Token]]:
    """Creates a new database token for a given workspace and for the authorized user.

    Args:
        json_body (TokenCreate): A mixin that allows us to rename the `group` field to `workspace`
            when serializing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTokenResponse400, Token]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: TokenCreate,
) -> Optional[Union[CreateDatabaseTokenResponse400, Token]]:
    """Creates a new database token for a given workspace and for the authorized user.

    Args:
        json_body (TokenCreate): A mixin that allows us to rename the `group` field to `workspace`
            when serializing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTokenResponse400, Token]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
