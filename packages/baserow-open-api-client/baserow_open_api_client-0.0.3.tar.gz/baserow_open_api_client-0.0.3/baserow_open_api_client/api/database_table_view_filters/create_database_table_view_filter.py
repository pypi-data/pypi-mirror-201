from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_table_view_filter_response_400 import CreateDatabaseTableViewFilterResponse400
from ...models.create_database_table_view_filter_response_404 import CreateDatabaseTableViewFilterResponse404
from ...models.create_view_filter import CreateViewFilter
from ...models.view_filter import ViewFilter
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreateViewFilter,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/filters/".format(client.base_url, view_id=view_id)

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
) -> Optional[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ViewFilter.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableViewFilterResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableViewFilterResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
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
    json_body: CreateViewFilter,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
    """Creates a new filter for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, then only the rows that apply to all the
    filters are going to be returned. A filter compares the value of a field to the value of a filter.
    It depends on the type how values are going to be compared.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]
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
    json_body: CreateViewFilter,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
    """Creates a new filter for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, then only the rows that apply to all the
    filters are going to be returned. A filter compares the value of a field to the value of a filter.
    It depends on the type how values are going to be compared.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]
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
    json_body: CreateViewFilter,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
    """Creates a new filter for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, then only the rows that apply to all the
    filters are going to be returned. A filter compares the value of a field to the value of a filter.
    It depends on the type how values are going to be compared.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]
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
    json_body: CreateViewFilter,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]]:
    """Creates a new filter for the view related to the provided `view_id` parameter if the authorized user
    has access to the related database's workspace. When the rows of a view are requested, for example
    via the `list_database_table_grid_view_rows` endpoint, then only the rows that apply to all the
    filters are going to be returned. A filter compares the value of a field to the value of a filter.
    It depends on the type how values are going to be compared.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (CreateViewFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewFilterResponse400, CreateDatabaseTableViewFilterResponse404, ViewFilter]
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
