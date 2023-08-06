from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.calendar_view_field_options_wrapper import CalendarViewFieldOptionsWrapper
from ...models.form_view_field_options_wrapper import FormViewFieldOptionsWrapper
from ...models.gallery_view_field_options_wrapper import GalleryViewFieldOptionsWrapper
from ...models.get_database_table_view_field_options_response_400 import GetDatabaseTableViewFieldOptionsResponse400
from ...models.get_database_table_view_field_options_response_404 import GetDatabaseTableViewFieldOptionsResponse404
from ...models.grid_view_field_options_wrapper import GridViewFieldOptionsWrapper
from ...models.kanban_view_field_options_wrapper import KanbanViewFieldOptionsWrapper
from ...types import Response


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/field-options/".format(client.base_url, view_id=view_id)

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
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
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
        response_400 = GetDatabaseTableViewFieldOptionsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseTableViewFieldOptionsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
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
) -> Response[
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
    ]
]:
    """Responds with the fields options of the provided view if the authenticated user has access to the
    related workspace.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableViewFieldOptionsResponse400, GetDatabaseTableViewFieldOptionsResponse404, Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper']]]
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
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
    ]
]:
    """Responds with the fields options of the provided view if the authenticated user has access to the
    related workspace.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableViewFieldOptionsResponse400, GetDatabaseTableViewFieldOptionsResponse404, Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper']]
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
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
    ]
]:
    """Responds with the fields options of the provided view if the authenticated user has access to the
    related workspace.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseTableViewFieldOptionsResponse400, GetDatabaseTableViewFieldOptionsResponse404, Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper']]]
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
    Union[
        GetDatabaseTableViewFieldOptionsResponse400,
        GetDatabaseTableViewFieldOptionsResponse404,
        Union[
            "CalendarViewFieldOptionsWrapper",
            "FormViewFieldOptionsWrapper",
            "GalleryViewFieldOptionsWrapper",
            "GridViewFieldOptionsWrapper",
            "KanbanViewFieldOptionsWrapper",
        ],
    ]
]:
    """Responds with the fields options of the provided view if the authenticated user has access to the
    related workspace.

    Args:
        view_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseTableViewFieldOptionsResponse400, GetDatabaseTableViewFieldOptionsResponse404, Union['CalendarViewFieldOptionsWrapper', 'FormViewFieldOptionsWrapper', 'GalleryViewFieldOptionsWrapper', 'GridViewFieldOptionsWrapper', 'KanbanViewFieldOptionsWrapper']]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
        )
    ).parsed
