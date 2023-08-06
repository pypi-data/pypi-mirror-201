from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_fill_remaining_seats_of_license_response_400 import AdminFillRemainingSeatsOfLicenseResponse400
from ...models.admin_fill_remaining_seats_of_license_response_404 import AdminFillRemainingSeatsOfLicenseResponse404
from ...models.license_user import LicenseUser
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/licenses/{id}/fill-seats/".format(client.base_url, id=id)

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
) -> Optional[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LicenseUser.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminFillRemainingSeatsOfLicenseResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminFillRemainingSeatsOfLicenseResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
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
) -> Response[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
    """Fills the remaining empty seats of the license with the first users that are found.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List['LicenseUser']]]
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
) -> Optional[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
    """Fills the remaining empty seats of the license with the first users that are found.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List['LicenseUser']]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
    """Fills the remaining empty seats of the license with the first users that are found.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List['LicenseUser']]]
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
) -> Optional[
    Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List["LicenseUser"]]
]:
    """Fills the remaining empty seats of the license with the first users that are found.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminFillRemainingSeatsOfLicenseResponse400, AdminFillRemainingSeatsOfLicenseResponse404, List['LicenseUser']]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
