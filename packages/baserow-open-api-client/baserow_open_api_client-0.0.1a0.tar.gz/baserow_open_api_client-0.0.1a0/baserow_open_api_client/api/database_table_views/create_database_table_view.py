from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_create_view import CalendarViewCreateView
from ...models.calendar_view_view import CalendarViewView
from ...models.create_database_table_view_response_400 import CreateDatabaseTableViewResponse400
from ...models.create_database_table_view_response_404 import CreateDatabaseTableViewResponse404
from ...models.form_view_create_view import FormViewCreateView
from ...models.form_view_view import FormViewView
from ...models.gallery_view_create_view import GalleryViewCreateView
from ...models.gallery_view_view import GalleryViewView
from ...models.grid_view_create_view import GridViewCreateView
from ...models.grid_view_view import GridViewView
from ...models.kanban_view_create_view import KanbanViewCreateView
from ...models.kanban_view_view import KanbanViewView
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewCreateView",
        "FormViewCreateView",
        "GalleryViewCreateView",
        "GridViewCreateView",
        "KanbanViewCreateView",
    ],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/table/{table_id}/".format(client.base_url, table_id=table_id)

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

    if isinstance(json_body, GridViewCreateView):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, GalleryViewCreateView):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, FormViewCreateView):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, KanbanViewCreateView):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    result = {
        "method": "post",
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
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
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
        response_400 = CreateDatabaseTableViewResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
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
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewCreateView",
        "FormViewCreateView",
        "GalleryViewCreateView",
        "GridViewCreateView",
        "KanbanViewCreateView",
    ],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Creates a new view for the table related to the provided `table_id` parameter if the authorized user
    has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewCreateView', 'FormViewCreateView', 'GalleryViewCreateView',
            'GridViewCreateView', 'KanbanViewCreateView']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewResponse400, CreateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        include=include,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    json_body: Union[
        "CalendarViewCreateView",
        "FormViewCreateView",
        "GalleryViewCreateView",
        "GridViewCreateView",
        "KanbanViewCreateView",
    ],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Creates a new view for the table related to the provided `table_id` parameter if the authorized user
    has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewCreateView', 'FormViewCreateView', 'GalleryViewCreateView',
            'GridViewCreateView', 'KanbanViewCreateView']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewResponse400, CreateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
        include=include,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewCreateView",
        "FormViewCreateView",
        "GalleryViewCreateView",
        "GridViewCreateView",
        "KanbanViewCreateView",
    ],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Creates a new view for the table related to the provided `table_id` parameter if the authorized user
    has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewCreateView', 'FormViewCreateView', 'GalleryViewCreateView',
            'GridViewCreateView', 'KanbanViewCreateView']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewResponse400, CreateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
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
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewCreateView",
        "FormViewCreateView",
        "GalleryViewCreateView",
        "GridViewCreateView",
        "KanbanViewCreateView",
    ],
    include: Union[Unset, None, str] = UNSET,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableViewResponse400,
        CreateDatabaseTableViewResponse404,
        Union["CalendarViewView", "FormViewView", "GalleryViewView", "GridViewView", "KanbanViewView"],
    ]
]:
    """Creates a new view for the table related to the provided `table_id` parameter if the authorized user
    has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.

    Args:
        table_id (int):
        include (Union[Unset, None, str]):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewCreateView', 'FormViewCreateView', 'GalleryViewCreateView',
            'GridViewCreateView', 'KanbanViewCreateView']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewResponse400, CreateDatabaseTableViewResponse404, Union['CalendarViewView', 'FormViewView', 'GalleryViewView', 'GridViewView', 'KanbanViewView']]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
            include=include,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
