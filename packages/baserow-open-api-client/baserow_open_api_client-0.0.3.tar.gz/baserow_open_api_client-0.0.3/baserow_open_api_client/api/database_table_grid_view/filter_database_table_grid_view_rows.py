from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.example_row_response import ExampleRowResponse
from ...models.filter_database_table_grid_view_rows_response_400 import FilterDatabaseTableGridViewRowsResponse400
from ...models.filter_database_table_grid_view_rows_response_404 import FilterDatabaseTableGridViewRowsResponse404
from ...models.grid_view_filter import GridViewFilter
from ...types import Response


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: GridViewFilter,
) -> Dict[str, Any]:
    url = "{}/api/database/views/grid/{view_id}/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    result = {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExampleRowResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = FilterDatabaseTableGridViewRowsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = FilterDatabaseTableGridViewRowsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
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
    json_body: GridViewFilter,
) -> Response[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
    ]
]:
    """Lists only the rows and fields that match the request. Only the rows with the ids that are in the
    `row_ids` list are going to be returned. Same goes for the fields, only the fields with the ids in
    the `field_ids` are going to be returned. This endpoint could be used to refresh data after changes
    something. For example in the web frontend after changing a field type, the data of the related
    cells will be refreshed using this endpoint. In the example all field types are listed, but normally
    the number in field_{id} key is going to be the id of the field. The value is what the user has
    provided and the format of it depends on the fields type.

    Args:
        view_id (int):
        json_body (GridViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FilterDatabaseTableGridViewRowsResponse400, FilterDatabaseTableGridViewRowsResponse404, List['ExampleRowResponse']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
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
    json_body: GridViewFilter,
) -> Optional[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
    ]
]:
    """Lists only the rows and fields that match the request. Only the rows with the ids that are in the
    `row_ids` list are going to be returned. Same goes for the fields, only the fields with the ids in
    the `field_ids` are going to be returned. This endpoint could be used to refresh data after changes
    something. For example in the web frontend after changing a field type, the data of the related
    cells will be refreshed using this endpoint. In the example all field types are listed, but normally
    the number in field_{id} key is going to be the id of the field. The value is what the user has
    provided and the format of it depends on the fields type.

    Args:
        view_id (int):
        json_body (GridViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FilterDatabaseTableGridViewRowsResponse400, FilterDatabaseTableGridViewRowsResponse404, List['ExampleRowResponse']]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: GridViewFilter,
) -> Response[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
    ]
]:
    """Lists only the rows and fields that match the request. Only the rows with the ids that are in the
    `row_ids` list are going to be returned. Same goes for the fields, only the fields with the ids in
    the `field_ids` are going to be returned. This endpoint could be used to refresh data after changes
    something. For example in the web frontend after changing a field type, the data of the related
    cells will be refreshed using this endpoint. In the example all field types are listed, but normally
    the number in field_{id} key is going to be the id of the field. The value is what the user has
    provided and the format of it depends on the fields type.

    Args:
        view_id (int):
        json_body (GridViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FilterDatabaseTableGridViewRowsResponse400, FilterDatabaseTableGridViewRowsResponse404, List['ExampleRowResponse']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: GridViewFilter,
) -> Optional[
    Union[
        FilterDatabaseTableGridViewRowsResponse400,
        FilterDatabaseTableGridViewRowsResponse404,
        List["ExampleRowResponse"],
    ]
]:
    """Lists only the rows and fields that match the request. Only the rows with the ids that are in the
    `row_ids` list are going to be returned. Same goes for the fields, only the fields with the ids in
    the `field_ids` are going to be returned. This endpoint could be used to refresh data after changes
    something. For example in the web frontend after changing a field type, the data of the related
    cells will be refreshed using this endpoint. In the example all field types are listed, but normally
    the number in field_{id} key is going to be the id of the field. The value is what the user has
    provided and the format of it depends on the fields type.

    Args:
        view_id (int):
        json_body (GridViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FilterDatabaseTableGridViewRowsResponse400, FilterDatabaseTableGridViewRowsResponse404, List['ExampleRowResponse']]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
