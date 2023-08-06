from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_database_table_grid_view_field_aggregations_response_200 import (
    GetDatabaseTableGridViewFieldAggregationsResponse200,
)
from ...models.get_database_table_grid_view_field_aggregations_response_400 import (
    GetDatabaseTableGridViewFieldAggregationsResponse400,
)
from ...models.get_database_table_grid_view_field_aggregations_response_404 import (
    GetDatabaseTableGridViewFieldAggregationsResponse404,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/grid/{view_id}/aggregations/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["include"] = include

    params["search"] = search

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
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDatabaseTableGridViewFieldAggregationsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetDatabaseTableGridViewFieldAggregationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseTableGridViewFieldAggregationsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
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
    include: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
    ]
]:
    """Returns all field aggregations values previously defined for this grid view. If filters exist for
    this view, the aggregations are computed only on filtered rows.You need to have read permissions on
    the view to request aggregations.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableGridViewFieldAggregationsResponse200, GetDatabaseTableGridViewFieldAggregationsResponse400, GetDatabaseTableGridViewFieldAggregationsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        include=include,
        search=search,
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
    include: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
    ]
]:
    """Returns all field aggregations values previously defined for this grid view. If filters exist for
    this view, the aggregations are computed only on filtered rows.You need to have read permissions on
    the view to request aggregations.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableGridViewFieldAggregationsResponse200, GetDatabaseTableGridViewFieldAggregationsResponse400, GetDatabaseTableGridViewFieldAggregationsResponse404]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        include=include,
        search=search,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
    ]
]:
    """Returns all field aggregations values previously defined for this grid view. If filters exist for
    this view, the aggregations are computed only on filtered rows.You need to have read permissions on
    the view to request aggregations.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableGridViewFieldAggregationsResponse200, GetDatabaseTableGridViewFieldAggregationsResponse400, GetDatabaseTableGridViewFieldAggregationsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        include=include,
        search=search,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        GetDatabaseTableGridViewFieldAggregationsResponse200,
        GetDatabaseTableGridViewFieldAggregationsResponse400,
        GetDatabaseTableGridViewFieldAggregationsResponse404,
    ]
]:
    """Returns all field aggregations values previously defined for this grid view. If filters exist for
    this view, the aggregations are computed only on filtered rows.You need to have read permissions on
    the view to request aggregations.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableGridViewFieldAggregationsResponse200, GetDatabaseTableGridViewFieldAggregationsResponse400, GetDatabaseTableGridViewFieldAggregationsResponse404]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            include=include,
            search=search,
        )
    ).parsed
