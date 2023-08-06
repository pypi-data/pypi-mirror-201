from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_table_view_filters_response_400 import ListDatabaseTableViewFiltersResponse400
from ...models.list_database_table_view_filters_response_404 import ListDatabaseTableViewFiltersResponse404
from ...models.view_filter import ViewFilter
from ...types import Response


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/filters/".format(client.base_url, view_id=view_id)

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
) -> Optional[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ViewFilter.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableViewFiltersResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableViewFiltersResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
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
) -> Response[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
]:
    """Lists all filters of the view related to the provided `view_id` if the user has access to the
    related database's workspace. A view can have multiple filters. When all the rows are requested for
    the view only those that apply to the filters are returned.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List['ViewFilter']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
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
) -> Optional[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
]:
    """Lists all filters of the view related to the provided `view_id` if the user has access to the
    related database's workspace. A view can have multiple filters. When all the rows are requested for
    the view only those that apply to the filters are returned.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List['ViewFilter']]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
]:
    """Lists all filters of the view related to the provided `view_id` if the user has access to the
    related database's workspace. A view can have multiple filters. When all the rows are requested for
    the view only those that apply to the filters are returned.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List['ViewFilter']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List["ViewFilter"]]
]:
    """Lists all filters of the view related to the provided `view_id` if the user has access to the
    related database's workspace. A view can have multiple filters. When all the rows are requested for
    the view only those that apply to the filters are returned.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableViewFiltersResponse400, ListDatabaseTableViewFiltersResponse404, List['ViewFilter']]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
        )
    ).parsed
