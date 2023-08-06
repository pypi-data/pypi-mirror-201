from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_update import CalendarViewUpdate
from ...models.calendar_view_view import CalendarViewView
from ...models.form_view_update import FormViewUpdate
from ...models.form_view_view import FormViewView
from ...models.gallery_view_update import GalleryViewUpdate
from ...models.gallery_view_view import GalleryViewView
from ...models.grid_view_update import GridViewUpdate
from ...models.grid_view_view import GridViewView
from ...models.kanban_view_update import KanbanViewUpdate
from ...models.kanban_view_view import KanbanViewView
from ...models.update_database_table_view_response_400 import UpdateDatabaseTableViewResponse400
from ...models.update_database_table_view_response_404 import UpdateDatabaseTableViewResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["CalendarViewUpdate", "FormViewUpdate", "GalleryViewUpdate", "GridViewUpdate", "KanbanViewUpdate"],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    params: Dict[str, Any] = {}
    params["include"] = include

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body: Dict[str, Any]

    if isinstance(json_body, GridViewUpdate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, GalleryViewUpdate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, FormViewUpdate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, KanbanViewUpdate):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    result = {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
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

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateDatabaseTableViewResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateDatabaseTableViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
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
    json_body: Union["CalendarViewUpdate", "FormViewUpdate", "GalleryViewUpdate", "GridViewUpdate", "KanbanViewUpdate"],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
    httpx_client=None,
) -> Response[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
    ]
]:
    """Updates the existing view if the authorized user has access to the related database's workspace. The
    type cannot be changed. It depends on the existing type which properties can be changed.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewUpdate', 'FormViewUpdate', 'GalleryViewUpdate',
            'GridViewUpdate', 'KanbanViewUpdate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView'], UpdateDatabaseTableViewResponse400, UpdateDatabaseTableViewResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
        include=include,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["CalendarViewUpdate", "FormViewUpdate", "GalleryViewUpdate", "GridViewUpdate", "KanbanViewUpdate"],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
    ]
]:
    """Updates the existing view if the authorized user has access to the related database's workspace. The
    type cannot be changed. It depends on the existing type which properties can be changed.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewUpdate', 'FormViewUpdate', 'GalleryViewUpdate',
            'GridViewUpdate', 'KanbanViewUpdate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView'], UpdateDatabaseTableViewResponse400, UpdateDatabaseTableViewResponse404]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        json_body=json_body,
        include=include,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["CalendarViewUpdate", "FormViewUpdate", "GalleryViewUpdate", "GridViewUpdate", "KanbanViewUpdate"],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
    ]
]:
    """Updates the existing view if the authorized user has access to the related database's workspace. The
    type cannot be changed. It depends on the existing type which properties can be changed.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewUpdate', 'FormViewUpdate', 'GalleryViewUpdate',
            'GridViewUpdate', 'KanbanViewUpdate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView'], UpdateDatabaseTableViewResponse400, UpdateDatabaseTableViewResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
        include=include,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["CalendarViewUpdate", "FormViewUpdate", "GalleryViewUpdate", "GridViewUpdate", "KanbanViewUpdate"],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
        UpdateDatabaseTableViewResponse400,
        UpdateDatabaseTableViewResponse404,
    ]
]:
    """Updates the existing view if the authorized user has access to the related database's workspace. The
    type cannot be changed. It depends on the existing type which properties can be changed.

    Args:
        view_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewUpdate', 'FormViewUpdate', 'GalleryViewUpdate',
            'GridViewUpdate', 'KanbanViewUpdate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView'], UpdateDatabaseTableViewResponse400, UpdateDatabaseTableViewResponse404]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            json_body=json_body,
            include=include,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
