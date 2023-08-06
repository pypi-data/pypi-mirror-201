from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_license_lookup_users_response_404 import AdminLicenseLookupUsersResponse404
from ...models.pagination_serializer_license_user_lookup import PaginationSerializerLicenseUserLookup
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/licenses/{id}/lookup-users/".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["search"] = search

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    result = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerLicenseUserLookup.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = AdminLicenseLookupUsersResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
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
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
    """This endpoint can be used to lookup users that can be added to a  license. Users that are already in
    the license are not returned here. Optionally a `search` query parameter can be provided to filter
    the results.

    Args:
        id (int):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        page=page,
        search=search,
        size=size,
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
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
    """This endpoint can be used to lookup users that can be added to a  license. Users that are already in
    the license are not returned here. Optionally a `search` query parameter can be provided to filter
    the results.

    Args:
        id (int):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]
    """

    return sync_detailed(
        id=id,
        client=client,
        page=page,
        search=search,
        size=size,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Response[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
    """This endpoint can be used to lookup users that can be added to a  license. Users that are already in
    the license are not returned here. Optionally a `search` query parameter can be provided to filter
    the results.

    Args:
        id (int):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        page=page,
        search=search,
        size=size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, None, int] = UNSET,
    search: Union[Unset, None, str] = UNSET,
    size: Union[Unset, None, int] = UNSET,
) -> Optional[Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]]:
    """This endpoint can be used to lookup users that can be added to a  license. Users that are already in
    the license are not returned here. Optionally a `search` query parameter can be provided to filter
    the results.

    Args:
        id (int):
        page (Union[Unset, None, int]):
        search (Union[Unset, None, str]):
        size (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminLicenseLookupUsersResponse404, PaginationSerializerLicenseUserLookup]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            page=page,
            search=search,
            size=size,
        )
    ).parsed
