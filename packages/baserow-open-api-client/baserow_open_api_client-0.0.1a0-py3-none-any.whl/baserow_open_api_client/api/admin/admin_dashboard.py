from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_dashboard import AdminDashboard
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/admin/dashboard/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[AdminDashboard, Any]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AdminDashboard.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[AdminDashboard, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminDashboard, Any]]:
    """Returns the new and active users for the last 24 hours, 7 days and 30 days. The `previous_` values
    are the values of the period before, so for example `previous_new_users_last_24_hours` are the new
    users that signed up from 48 to 24 hours ago. It can be used to calculate an increase or decrease in
    the amount of signups. A list of the new and active users for every day for the last 30 days is also
    included.

    This is a **premium** feature.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminDashboard, Any]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminDashboard, Any]]:
    """Returns the new and active users for the last 24 hours, 7 days and 30 days. The `previous_` values
    are the values of the period before, so for example `previous_new_users_last_24_hours` are the new
    users that signed up from 48 to 24 hours ago. It can be used to calculate an increase or decrease in
    the amount of signups. A list of the new and active users for every day for the last 30 days is also
    included.

    This is a **premium** feature.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminDashboard, Any]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[AdminDashboard, Any]]:
    """Returns the new and active users for the last 24 hours, 7 days and 30 days. The `previous_` values
    are the values of the period before, so for example `previous_new_users_last_24_hours` are the new
    users that signed up from 48 to 24 hours ago. It can be used to calculate an increase or decrease in
    the amount of signups. A list of the new and active users for every day for the last 30 days is also
    included.

    This is a **premium** feature.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminDashboard, Any]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AdminDashboard, Any]]:
    """Returns the new and active users for the last 24 hours, 7 days and 30 days. The `previous_` values
    are the values of the period before, so for example `previous_new_users_last_24_hours` are the new
    users that signed up from 48 to 24 hours ago. It can be used to calculate an increase or decrease in
    the amount of signups. A list of the new and active users for every day for the last 30 days is also
    included.

    This is a **premium** feature.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminDashboard, Any]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
