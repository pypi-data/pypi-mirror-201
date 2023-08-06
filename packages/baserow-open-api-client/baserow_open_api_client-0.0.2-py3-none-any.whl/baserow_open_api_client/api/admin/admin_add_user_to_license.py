from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_add_user_to_license_response_400 import AdminAddUserToLicenseResponse400
from ...models.admin_add_user_to_license_response_404 import AdminAddUserToLicenseResponse404
from ...models.license_user import LicenseUser
from ...types import Response


def _get_kwargs(
    id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/licenses/{id}/{user_id}/".format(client.base_url, id=id, user_id=user_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "post",
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
) -> Optional[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LicenseUser.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminAddUserToLicenseResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminAddUserToLicenseResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    """Adds the user related to the provided parameter and to the license related to the parameter. This
    only happens if there are enough seats left on the license and if the user is not already on the
    license.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    """Adds the user related to the provided parameter and to the license related to the parameter. This
    only happens if there are enough seats left on the license and if the user is not already on the
    license.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]
    """

    return sync_detailed(
        id=id,
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    """Adds the user related to the provided parameter and to the license related to the parameter. This
    only happens if there are enough seats left on the license and if the user is not already on the
    license.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    user_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]]:
    """Adds the user related to the provided parameter and to the license related to the parameter. This
    only happens if there are enough seats left on the license and if the user is not already on the
    license.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminAddUserToLicenseResponse400, AdminAddUserToLicenseResponse404, LicenseUser]
    """

    return (
        await asyncio_detailed(
            id=id,
            user_id=user_id,
            client=client,
        )
    ).parsed
