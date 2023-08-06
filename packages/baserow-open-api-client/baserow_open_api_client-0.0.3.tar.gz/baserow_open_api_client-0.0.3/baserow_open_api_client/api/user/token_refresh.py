from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.token_refresh_response_200 import TokenRefreshResponse200
from ...models.token_refresh_with_user import TokenRefreshWithUser
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: TokenRefreshWithUser,
) -> Dict[str, Any]:
    url = "{}/api/user/token-refresh/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, TokenRefreshResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenRefreshResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, response.json())
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, TokenRefreshResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: TokenRefreshWithUser,
) -> Response[Union[Any, TokenRefreshResponse200]]:
    """Generate a new access_token that can be used to continue operating on Baserow starting from a valid
    refresh token.

    Args:
        json_body (TokenRefreshWithUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TokenRefreshResponse200]]
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
    client: Client,
    json_body: TokenRefreshWithUser,
) -> Optional[Union[Any, TokenRefreshResponse200]]:
    """Generate a new access_token that can be used to continue operating on Baserow starting from a valid
    refresh token.

    Args:
        json_body (TokenRefreshWithUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TokenRefreshResponse200]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: TokenRefreshWithUser,
) -> Response[Union[Any, TokenRefreshResponse200]]:
    """Generate a new access_token that can be used to continue operating on Baserow starting from a valid
    refresh token.

    Args:
        json_body (TokenRefreshWithUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, TokenRefreshResponse200]]
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
    client: Client,
    json_body: TokenRefreshWithUser,
) -> Optional[Union[Any, TokenRefreshResponse200]]:
    """Generate a new access_token that can be used to continue operating on Baserow starting from a valid
    refresh token.

    Args:
        json_body (TokenRefreshWithUser):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, TokenRefreshResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
