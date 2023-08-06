from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_view import CalendarViewView
from ...models.duplicate_database_table_view_response_400 import DuplicateDatabaseTableViewResponse400
from ...models.duplicate_database_table_view_response_404 import DuplicateDatabaseTableViewResponse404
from ...models.form_view_view import FormViewView
from ...models.gallery_view_view import GalleryViewView
from ...models.grid_view_view import GridViewView
from ...models.kanban_view_view import KanbanViewView
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/duplicate/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    result = {
        "method": "post",
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
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
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
        response_400 = DuplicateDatabaseTableViewResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DuplicateDatabaseTableViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
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
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Duplicates an existing view if the user has access to it. When a view is duplicated everything is
    copied except:
    - The name is appended with the copy number. Ex: `ViewName`->`ViewName(2)` and `View(2)`->`View(3)`
    - If the original view is publicly shared, the new view will not be shared anymore

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateDatabaseTableViewResponse400, DuplicateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Duplicates an existing view if the user has access to it. When a view is duplicated everything is
    copied except:
    - The name is appended with the copy number. Ex: `ViewName`->`ViewName(2)` and `View(2)`->`View(3)`
    - If the original view is publicly shared, the new view will not be shared anymore

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateDatabaseTableViewResponse400, DuplicateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Duplicates an existing view if the user has access to it. When a view is duplicated everything is
    copied except:
    - The name is appended with the copy number. Ex: `ViewName`->`ViewName(2)` and `View(2)`->`View(3)`
    - If the original view is publicly shared, the new view will not be shared anymore

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateDatabaseTableViewResponse400, DuplicateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
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
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        DuplicateDatabaseTableViewResponse400,
        DuplicateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Duplicates an existing view if the user has access to it. When a view is duplicated everything is
    copied except:
    - The name is appended with the copy number. Ex: `ViewName`->`ViewName(2)` and `View(2)`->`View(3)`
    - If the original view is publicly shared, the new view will not be shared anymore

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateDatabaseTableViewResponse400, DuplicateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
