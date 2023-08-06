from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_remove_all_users_from_license_response_400 import AdminRemoveAllUsersFromLicenseResponse400
from ...models.admin_remove_all_users_from_license_response_404 import AdminRemoveAllUsersFromLicenseResponse404
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/licenses/{id}/remove-all-users/".format(client.base_url, id=id)

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
) -> Optional[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminRemoveAllUsersFromLicenseResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminRemoveAllUsersFromLicenseResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    """Removes all the users that are on the license. This will empty all the seats.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    """Removes all the users that are on the license. This will empty all the seats.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    """Removes all the users that are on the license. This will empty all the seats.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]]:
    """Removes all the users that are on the license. This will empty all the seats.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminRemoveAllUsersFromLicenseResponse400, AdminRemoveAllUsersFromLicenseResponse404, Any]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
