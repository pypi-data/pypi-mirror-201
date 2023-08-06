from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_database_table_grid_view_field_aggregation_response_200 import (
    GetDatabaseTableGridViewFieldAggregationResponse200,
)
from ...models.get_database_table_grid_view_field_aggregation_response_400 import (
    GetDatabaseTableGridViewFieldAggregationResponse400,
)
from ...models.get_database_table_grid_view_field_aggregation_response_404 import (
    GetDatabaseTableGridViewFieldAggregationResponse404,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    field_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/grid/{view_id}/aggregation/{field_id}/".format(
        client.base_url, view_id=view_id, field_id=field_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["include"] = include

    params["type"] = type

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
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDatabaseTableGridViewFieldAggregationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetDatabaseTableGridViewFieldAggregationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseTableGridViewFieldAggregationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
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
    field_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
    ]
]:
    """Computes the aggregation of all the values for a specified field from the selected grid view. You
    must select the aggregation type by setting the `type` GET parameter. If filters are configured for
    the selected view, the aggregation is calculated only on filtered rows. You need to have read
    permissions on the view to request an aggregation.

    Args:
        view_id (int):
        field_id (int):
        include (Union[Unset, None, str]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableGridViewFieldAggregationResponse200, GetDatabaseTableGridViewFieldAggregationResponse400, GetDatabaseTableGridViewFieldAggregationResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        field_id=field_id,
        client=client,
        include=include,
        type=type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    view_id: int,
    field_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
    ]
]:
    """Computes the aggregation of all the values for a specified field from the selected grid view. You
    must select the aggregation type by setting the `type` GET parameter. If filters are configured for
    the selected view, the aggregation is calculated only on filtered rows. You need to have read
    permissions on the view to request an aggregation.

    Args:
        view_id (int):
        field_id (int):
        include (Union[Unset, None, str]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableGridViewFieldAggregationResponse200, GetDatabaseTableGridViewFieldAggregationResponse400, GetDatabaseTableGridViewFieldAggregationResponse404]
    """

    return sync_detailed(
        view_id=view_id,
        field_id=field_id,
        client=client,
        include=include,
        type=type,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    field_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
    ]
]:
    """Computes the aggregation of all the values for a specified field from the selected grid view. You
    must select the aggregation type by setting the `type` GET parameter. If filters are configured for
    the selected view, the aggregation is calculated only on filtered rows. You need to have read
    permissions on the view to request an aggregation.

    Args:
        view_id (int):
        field_id (int):
        include (Union[Unset, None, str]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableGridViewFieldAggregationResponse200, GetDatabaseTableGridViewFieldAggregationResponse400, GetDatabaseTableGridViewFieldAggregationResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        field_id=field_id,
        client=client,
        include=include,
        type=type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    field_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        GetDatabaseTableGridViewFieldAggregationResponse200,
        GetDatabaseTableGridViewFieldAggregationResponse400,
        GetDatabaseTableGridViewFieldAggregationResponse404,
    ]
]:
    """Computes the aggregation of all the values for a specified field from the selected grid view. You
    must select the aggregation type by setting the `type` GET parameter. If filters are configured for
    the selected view, the aggregation is calculated only on filtered rows. You need to have read
    permissions on the view to request an aggregation.

    Args:
        view_id (int):
        field_id (int):
        include (Union[Unset, None, str]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableGridViewFieldAggregationResponse200, GetDatabaseTableGridViewFieldAggregationResponse400, GetDatabaseTableGridViewFieldAggregationResponse404]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            field_id=field_id,
            client=client,
            include=include,
            type=type,
        )
    ).parsed
