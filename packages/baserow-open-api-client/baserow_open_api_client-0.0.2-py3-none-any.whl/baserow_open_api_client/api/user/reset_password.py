from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.reset_password_body_validation import ResetPasswordBodyValidation
from ...models.reset_password_response_400 import ResetPasswordResponse400
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ResetPasswordBodyValidation,
) -> Dict[str, Any]:
    url = "{}/api/user/reset-password/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, ResetPasswordResponse400]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ResetPasswordResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, ResetPasswordResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ResetPasswordBodyValidation,
) -> Response[Union[Any, ResetPasswordResponse400]]:
    """Changes the password of a user if the reset token is valid. The **send_password_reset_email**
    endpoint sends an email to the user containing the token. That token can be used to change the
    password here without providing the old password.

    Args:
        json_body (ResetPasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResetPasswordResponse400]]
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
    json_body: ResetPasswordBodyValidation,
) -> Optional[Union[Any, ResetPasswordResponse400]]:
    """Changes the password of a user if the reset token is valid. The **send_password_reset_email**
    endpoint sends an email to the user containing the token. That token can be used to change the
    password here without providing the old password.

    Args:
        json_body (ResetPasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResetPasswordResponse400]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ResetPasswordBodyValidation,
) -> Response[Union[Any, ResetPasswordResponse400]]:
    """Changes the password of a user if the reset token is valid. The **send_password_reset_email**
    endpoint sends an email to the user containing the token. That token can be used to change the
    password here without providing the old password.

    Args:
        json_body (ResetPasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ResetPasswordResponse400]]
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
    json_body: ResetPasswordBodyValidation,
) -> Optional[Union[Any, ResetPasswordResponse400]]:
    """Changes the password of a user if the reset token is valid. The **send_password_reset_email**
    endpoint sends an email to the user containing the token. That token can be used to change the
    password here without providing the old password.

    Args:
        json_body (ResetPasswordBodyValidation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ResetPasswordResponse400]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
