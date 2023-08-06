from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_password_body_validation import ChangePasswordBodyValidation
from ...models.change_password_response_400 import ChangePasswordResponse400
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ChangePasswordBodyValidation,
) -> Dict[str, Any]:
    url = "{}/api/user/change-password/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, ChangePasswordResponse400]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ChangePasswordResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, ChangePasswordResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, json_body: ChangePasswordBodyValidation, httpx_client=None
) -> Response[Union[Any, ChangePasswordResponse400]]:
    """Changes the password of an authenticated user, but only if the old password matches.

    Args:
        json_body (ChangePasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChangePasswordResponse400]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = (httpx_client or httpx).request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ChangePasswordBodyValidation,
) -> Optional[Union[Any, ChangePasswordResponse400]]:
    """Changes the password of an authenticated user, but only if the old password matches.

    Args:
        json_body (ChangePasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChangePasswordResponse400]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ChangePasswordBodyValidation,
) -> Response[Union[Any, ChangePasswordResponse400]]:
    """Changes the password of an authenticated user, but only if the old password matches.

    Args:
        json_body (ChangePasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChangePasswordResponse400]]
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
    json_body: ChangePasswordBodyValidation,
) -> Optional[Union[Any, ChangePasswordResponse400]]:
    """Changes the password of an authenticated user, but only if the old password matches.

    Args:
        json_body (ChangePasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChangePasswordResponse400]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
