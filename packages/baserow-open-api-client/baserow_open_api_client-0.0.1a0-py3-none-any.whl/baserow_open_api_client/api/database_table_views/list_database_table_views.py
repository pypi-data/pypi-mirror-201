from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_view import CalendarViewView
from ...models.form_view_view import FormViewView
from ...models.gallery_view_view import GalleryViewView
from ...models.grid_view_view import GridViewView
from ...models.kanban_view_view import KanbanViewView
from ...models.list_database_table_views_response_400 import ListDatabaseTableViewsResponse400
from ...models.list_database_table_views_response_404 import ListDatabaseTableViewsResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/table/{table_id}/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["include"] = include

    params["limit"] = limit

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
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_view_view_type_0 = GridViewView.from_dict(data)

                    return componentsschemas_view_view_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_view_view_type_1 = GalleryViewView.from_dict(data)

                    return componentsschemas_view_view_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_view_view_type_2 = FormViewView.from_dict(data)

                    return componentsschemas_view_view_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_view_view_type_3 = KanbanViewView.from_dict(data)

                    return componentsschemas_view_view_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_view_view_type_4 = CalendarViewView.from_dict(data)

                return componentsschemas_view_view_type_4

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableViewsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableViewsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    """Lists all views of the table related to the provided `table_id` if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table can have multiple views. Each view can display the data in a different
    way. For example the `grid` view shows the in a spreadsheet like way. That type has custom endpoints
    for data retrieval and manipulation. In the future other views types like a calendar or Kanban are
    going to be added. Each type can have different properties.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableViewsResponse400, ListDatabaseTableViewsResponse404, List[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        include=include,
        limit=limit,
        type=type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    table_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    """Lists all views of the table related to the provided `table_id` if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table can have multiple views. Each view can display the data in a different
    way. For example the `grid` view shows the in a spreadsheet like way. That type has custom endpoints
    for data retrieval and manipulation. In the future other views types like a calendar or Kanban are
    going to be added. Each type can have different properties.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableViewsResponse400, ListDatabaseTableViewsResponse404, List[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        include=include,
        limit=limit,
        type=type,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    """Lists all views of the table related to the provided `table_id` if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table can have multiple views. Each view can display the data in a different
    way. For example the `grid` view shows the in a spreadsheet like way. That type has custom endpoints
    for data retrieval and manipulation. In the future other views types like a calendar or Kanban are
    going to be added. Each type can have different properties.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableViewsResponse400, ListDatabaseTableViewsResponse404, List[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        include=include,
        limit=limit,
        type=type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    include: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    type: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableViewsResponse400,
        ListDatabaseTableViewsResponse404,
        List[Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"]],
    ]
]:
    """Lists all views of the table related to the provided `table_id` if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table can have multiple views. Each view can display the data in a different
    way. For example the `grid` view shows the in a spreadsheet like way. That type has custom endpoints
    for data retrieval and manipulation. In the future other views types like a calendar or Kanban are
    going to be added. Each type can have different properties.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        type (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableViewsResponse400, ListDatabaseTableViewsResponse404, List[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            include=include,
            limit=limit,
            type=type,
        )
    ).parsed
