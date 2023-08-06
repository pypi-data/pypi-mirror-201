import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_example_response import CalendarViewExampleResponse
from ...models.list_database_table_calendar_view_rows_response_400 import ListDatabaseTableCalendarViewRowsResponse400
from ...models.list_database_table_calendar_view_rows_response_404 import ListDatabaseTableCalendarViewRowsResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    from_timestamp: datetime.datetime,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
    to_timestamp: datetime.datetime,
    user_timezone: Union[Unset, None, str] = "UTC",
) -> Dict[str, Any]:
    url = "{}/api/database/views/calendar/{view_id}/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_from_timestamp = from_timestamp.isoformat()

    params["from_timestamp"] = json_from_timestamp

    params["include"] = include

    params["limit"] = limit

    params["offset"] = offset

    json_to_timestamp = to_timestamp.isoformat()

    params["to_timestamp"] = json_to_timestamp

    params["user_timezone"] = user_timezone

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
) -> Optional[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CalendarViewExampleResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableCalendarViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableCalendarViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    from_timestamp: datetime.datetime,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
    to_timestamp: datetime.datetime,
    user_timezone: Union[Unset, None, str] = "UTC",
) -> Response[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by date regarding view's date fieldif the user is
    authenticated and has access to the related workspace.

    This is a **premium** feature.

    Args:
        view_id (int):
        from_timestamp (datetime.datetime):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        to_timestamp (datetime.datetime):
        user_timezone (Union[Unset, None, str]):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CalendarViewExampleResponse, ListDatabaseTableCalendarViewRowsResponse400, ListDatabaseTableCalendarViewRowsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        from_timestamp=from_timestamp,
        include=include,
        limit=limit,
        offset=offset,
        to_timestamp=to_timestamp,
        user_timezone=user_timezone,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    view_id: int,
    *,
    client: AuthenticatedClient,
    from_timestamp: datetime.datetime,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
    to_timestamp: datetime.datetime,
    user_timezone: Union[Unset, None, str] = "UTC",
) -> Optional[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by date regarding view's date fieldif the user is
    authenticated and has access to the related workspace.

    This is a **premium** feature.

    Args:
        view_id (int):
        from_timestamp (datetime.datetime):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        to_timestamp (datetime.datetime):
        user_timezone (Union[Unset, None, str]):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CalendarViewExampleResponse, ListDatabaseTableCalendarViewRowsResponse400, ListDatabaseTableCalendarViewRowsResponse404]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        from_timestamp=from_timestamp,
        include=include,
        limit=limit,
        offset=offset,
        to_timestamp=to_timestamp,
        user_timezone=user_timezone,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    from_timestamp: datetime.datetime,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
    to_timestamp: datetime.datetime,
    user_timezone: Union[Unset, None, str] = "UTC",
) -> Response[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by date regarding view's date fieldif the user is
    authenticated and has access to the related workspace.

    This is a **premium** feature.

    Args:
        view_id (int):
        from_timestamp (datetime.datetime):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        to_timestamp (datetime.datetime):
        user_timezone (Union[Unset, None, str]):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CalendarViewExampleResponse, ListDatabaseTableCalendarViewRowsResponse400, ListDatabaseTableCalendarViewRowsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        from_timestamp=from_timestamp,
        include=include,
        limit=limit,
        offset=offset,
        to_timestamp=to_timestamp,
        user_timezone=user_timezone,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    from_timestamp: datetime.datetime,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    offset: Union[Unset, None, int] = 0,
    to_timestamp: datetime.datetime,
    user_timezone: Union[Unset, None, str] = "UTC",
) -> Optional[
    Union[
        CalendarViewExampleResponse,
        ListDatabaseTableCalendarViewRowsResponse400,
        ListDatabaseTableCalendarViewRowsResponse404,
    ]
]:
    """Responds with serialized rows grouped by date regarding view's date fieldif the user is
    authenticated and has access to the related workspace.

    This is a **premium** feature.

    Args:
        view_id (int):
        from_timestamp (datetime.datetime):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        offset (Union[Unset, None, int]):
        to_timestamp (datetime.datetime):
        user_timezone (Union[Unset, None, str]):  Default: 'UTC'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CalendarViewExampleResponse, ListDatabaseTableCalendarViewRowsResponse400, ListDatabaseTableCalendarViewRowsResponse404]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            from_timestamp=from_timestamp,
            include=include,
            limit=limit,
            offset=offset,
            to_timestamp=to_timestamp,
            user_timezone=user_timezone,
        )
    ).parsed
