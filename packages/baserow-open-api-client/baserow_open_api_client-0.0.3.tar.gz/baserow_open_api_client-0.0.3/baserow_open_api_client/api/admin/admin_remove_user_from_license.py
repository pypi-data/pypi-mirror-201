from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_remove_user_from_license_response_400 import AdminRemoveUserFromLicenseResponse400
from ...models.admin_remove_user_from_license_response_404 import AdminRemoveUserFromLicenseResponse404
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
        "method": "delete",
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
) -> Optional[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminRemoveUserFromLicenseResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminRemoveUserFromLicenseResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
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
) -> Response[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
    """Removes the user related to the provided parameter and to the license related to the parameter. This
    only happens if the user is on the license, otherwise nothing will happen.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]
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
) -> Optional[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
    """Removes the user related to the provided parameter and to the license related to the parameter. This
    only happens if the user is on the license, otherwise nothing will happen.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]
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
) -> Response[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
    """Removes the user related to the provided parameter and to the license related to the parameter. This
    only happens if the user is on the license, otherwise nothing will happen.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]
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
) -> Optional[Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]]:
    """Removes the user related to the provided parameter and to the license related to the parameter. This
    only happens if the user is on the license, otherwise nothing will happen.

    Args:
        id (int):
        user_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminRemoveUserFromLicenseResponse400, AdminRemoveUserFromLicenseResponse404, Any]
    """

    return (
        await asyncio_detailed(
            id=id,
            user_id=user_id,
            client=client,
        )
    ).parsed
