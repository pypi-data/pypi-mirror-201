from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_table_view_sort_response_400 import CreateDatabaseTableViewSortResponse400
from ...models.create_database_table_view_sort_response_404 import CreateDatabaseTableViewSortResponse404
from ...models.create_view_sort import CreateViewSort
from ...models.view_sort import ViewSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreateViewSort,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/sortings/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

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
) -> Optional[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ViewSort.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableViewSortResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableViewSortResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
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
    json_body: CreateViewSort,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
    """Creates a new sort for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, they will be returned in the respected order
    defined by all the sortings.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewSort):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]
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
    json_body: CreateViewSort,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
    """Creates a new sort for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, they will be returned in the respected order
    defined by all the sortings.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewSort):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]
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
    json_body: CreateViewSort,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
    """Creates a new sort for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, they will be returned in the respected order
    defined by all the sortings.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewSort):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]
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
    json_body: CreateViewSort,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]]:
    """Creates a new sort for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, they will be returned in the respected order
    defined by all the sortings.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewSort):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewSortResponse400, CreateDatabaseTableViewSortResponse404, ViewSort]
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
