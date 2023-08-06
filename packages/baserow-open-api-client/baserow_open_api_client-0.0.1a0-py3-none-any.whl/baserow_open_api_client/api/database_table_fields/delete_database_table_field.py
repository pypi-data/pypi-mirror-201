from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_database_table_field_response_400 import DeleteDatabaseTableFieldResponse400
from ...models.delete_database_table_field_response_404 import DeleteDatabaseTableFieldResponse404
from ...models.related_fields import RelatedFields
from ...types import UNSET, Response, Unset


def _get_kwargs(
    field_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/fields/{field_id}/".format(client.base_url, field_id=field_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    result = {
        "method": "delete",
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
) -> Optional[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RelatedFields.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DeleteDatabaseTableFieldResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteDatabaseTableFieldResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    """Deletes the existing field if the authorized user has access to the related database's workspace.
    Note that all the related data to that field is also deleted. Primary fields cannot be deleted
    because their value represents the row. If deleting the field causes other fields to change then the
    specificinstances of those fields will be included in the related fields response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
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
    field_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    """Deletes the existing field if the authorized user has access to the related database's workspace.
    Note that all the related data to that field is also deleted. Primary fields cannot be deleted
    because their value represents the row. If deleting the field causes other fields to change then the
    specificinstances of those fields will be included in the related fields response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]
    """

    return sync_detailed(
        field_id=field_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    """Deletes the existing field if the authorized user has access to the related database's workspace.
    Note that all the related data to that field is also deleted. Primary fields cannot be deleted
    because their value represents the row. If deleting the field causes other fields to change then the
    specificinstances of those fields will be included in the related fields response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    field_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]]:
    """Deletes the existing field if the authorized user has access to the related database's workspace.
    Note that all the related data to that field is also deleted. Primary fields cannot be deleted
    because their value represents the row. If deleting the field causes other fields to change then the
    specificinstances of those fields will be included in the related fields response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteDatabaseTableFieldResponse400, DeleteDatabaseTableFieldResponse404, RelatedFields]
    """

    return (
        await asyncio_detailed(
            field_id=field_id,
            client=client,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
