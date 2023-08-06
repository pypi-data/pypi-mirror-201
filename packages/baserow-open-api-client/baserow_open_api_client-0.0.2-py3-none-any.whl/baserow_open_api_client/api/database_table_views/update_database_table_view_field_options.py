from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_field_options_wrapper import CalendarViewFieldOptionsWrapper
from ...models.form_view_field_options_wrapper import FormViewFieldOptionsWrapper
from ...models.gallery_view_field_options_wrapper import GalleryViewFieldOptionsWrapper
from ...models.grid_view_field_options_wrapper import GridViewFieldOptionsWrapper
from ...models.kanban_view_field_options_wrapper import KanbanViewFieldOptionsWrapper
from ...models.update_database_table_view_field_options_response_400 import (
    UpdateDatabaseTableViewFieldOptionsResponse400,
)
from ...models.update_database_table_view_field_options_response_404 import (
    UpdateDatabaseTableViewFieldOptionsResponse404,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewFieldOptionsWrapper",
        "FormViewFieldOptionsWrapper",
        "GalleryViewFieldOptionsWrapper",
        "GridViewFieldOptionsWrapper",
        "KanbanViewFieldOptionsWrapper",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/field-options/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    json_json_body: Dict[str, Any]

    if isinstance(json_body, GridViewFieldOptionsWrapper):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, GalleryViewFieldOptionsWrapper):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, FormViewFieldOptionsWrapper):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, KanbanViewFieldOptionsWrapper):
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
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_view_field_options_type_0 = GridViewFieldOptionsWrapper.from_dict(data)

                return componentsschemas_view_field_options_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_view_field_options_type_1 = GalleryViewFieldOptionsWrapper.from_dict(data)

                return componentsschemas_view_field_options_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_view_field_options_type_2 = FormViewFieldOptionsWrapper.from_dict(data)

                return componentsschemas_view_field_options_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_view_field_options_type_3 = KanbanViewFieldOptionsWrapper.from_dict(data)

                return componentsschemas_view_field_options_type_3
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_view_field_options_type_4 = CalendarViewFieldOptionsWrapper.from_dict(data)

            return componentsschemas_view_field_options_type_4

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateDatabaseTableViewFieldOptionsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateDatabaseTableViewFieldOptionsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
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
    json_body: Union[
        "CalendarViewFieldOptionsWrapper",
        "FormViewFieldOptionsWrapper",
        "GalleryViewFieldOptionsWrapper",
        "GridViewFieldOptionsWrapper",
        "KanbanViewFieldOptionsWrapper",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
    ]
]:
    """Updates the field options of a view. The field options differ per field type  This could for example
    be used to update the field width of a `grid` view if the user changes it.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper',
            'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper',
            'KanbanViewFieldOptionsWrapper']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper'], UpdateDatabaseTableViewFieldOptionsResponse400, UpdateDatabaseTableViewFieldOptionsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
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
    json_body: Union[
        "CalendarViewFieldOptionsWrapper",
        "FormViewFieldOptionsWrapper",
        "GalleryViewFieldOptionsWrapper",
        "GridViewFieldOptionsWrapper",
        "KanbanViewFieldOptionsWrapper",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
    ]
]:
    """Updates the field options of a view. The field options differ per field type  This could for example
    be used to update the field width of a `grid` view if the user changes it.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper',
            'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper',
            'KanbanViewFieldOptionsWrapper']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper'], UpdateDatabaseTableViewFieldOptionsResponse400, UpdateDatabaseTableViewFieldOptionsResponse404]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "CalendarViewFieldOptionsWrapper",
        "FormViewFieldOptionsWrapper",
        "GalleryViewFieldOptionsWrapper",
        "GridViewFieldOptionsWrapper",
        "KanbanViewFieldOptionsWrapper",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
    ]
]:
    """Updates the field options of a view. The field options differ per field type  This could for example
    be used to update the field width of a `grid` view if the user changes it.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper',
            'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper',
            'KanbanViewFieldOptionsWrapper']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper'], UpdateDatabaseTableViewFieldOptionsResponse400, UpdateDatabaseTableViewFieldOptionsResponse404]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
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
    json_body: Union[
        "CalendarViewFieldOptionsWrapper",
        "FormViewFieldOptionsWrapper",
        "GalleryViewFieldOptionsWrapper",
        "GridViewFieldOptionsWrapper",
        "KanbanViewFieldOptionsWrapper",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
        UpdateDatabaseTableViewFieldOptionsResponse400,
        UpdateDatabaseTableViewFieldOptionsResponse404,
    ]
]:
    """Updates the field options of a view. The field options differ per field type  This could for example
    be used to update the field width of a `grid` view if the user changes it.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper',
            'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper',
            'KanbanViewFieldOptionsWrapper']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper'], UpdateDatabaseTableViewFieldOptionsResponse400, UpdateDatabaseTableViewFieldOptionsResponse404]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
