from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_license_check_response_404 import AdminLicenseCheckResponse404
from ...models.license_with_users import LicenseWithUsers
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/licenses/{id}/check/".format(client.base_url, id=id)

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
) -> Optional[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = LicenseWithUsers.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminLicenseCheckResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int, *, client: AuthenticatedClient, httpx_client=None
) -> Response[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    """This endpoint checks with the authority if the license needs to be updated. It also checks if the
    license is operating within its limits and might take action on that. It could also happen that the
    license has been deleted because there is an instance id mismatch or because it's invalid. In that
    case a `204` status code is returned.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]
    """

    kwargs = _get_kwargs(
        id=id,
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
    id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    """This endpoint checks with the authority if the license needs to be updated. It also checks if the
    license is operating within its limits and might take action on that. It could also happen that the
    license has been deleted because there is an instance id mismatch or because it's invalid. In that
    case a `204` status code is returned.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminLicenseCheckResponse404, LicenseWithUsers]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    """This endpoint checks with the authority if the license needs to be updated. It also checks if the
    license is operating within its limits and might take action on that. It could also happen that the
    license has been deleted because there is an instance id mismatch or because it's invalid. In that
    case a `204` status code is returned.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]
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
) -> Optional[Union[AdminLicenseCheckResponse404, LicenseWithUsers]]:
    """This endpoint checks with the authority if the license needs to be updated. It also checks if the
    license is operating within its limits and might take action on that. It could also happen that the
    license has been deleted because there is an instance id mismatch or because it's invalid. In that
    case a `204` status code is returned.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminLicenseCheckResponse404, LicenseWithUsers]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
