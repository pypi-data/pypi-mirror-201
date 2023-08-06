from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.application_create import ApplicationCreate
from ...models.builder_application import BuilderApplication
from ...models.database_application import DatabaseApplication
from ...models.workspace_create_application_response_400 import WorkspaceCreateApplicationResponse400
from ...models.workspace_create_application_response_404 import WorkspaceCreateApplicationResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ApplicationCreate,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/applications/workspace/{workspace_id}/".format(client.base_url, workspace_id=workspace_id)

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
) -> Optional[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["BuilderApplication", "DatabaseApplication"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_applications_type_0 = DatabaseApplication.from_dict(data)

                return componentsschemas_applications_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_applications_type_1 = BuilderApplication.from_dict(data)

            return componentsschemas_applications_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = WorkspaceCreateApplicationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = WorkspaceCreateApplicationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ApplicationCreate,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
    httpx_client=None,
) -> Response[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    """Creates a new application based on the provided type. The newly created application is going to be
    added to the workspace related to the provided `workspace_id` parameter. If the authorized user does
    not belong to the workspace an error will be returned.

    Args:
        workspace_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ApplicationCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['BuilderApplication', 'DatabaseApplication'], WorkspaceCreateApplicationResponse400, WorkspaceCreateApplicationResponse404]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
        json_body=json_body,
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
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ApplicationCreate,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    """Creates a new application based on the provided type. The newly created application is going to be
    added to the workspace related to the provided `workspace_id` parameter. If the authorized user does
    not belong to the workspace an error will be returned.

    Args:
        workspace_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ApplicationCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['BuilderApplication', 'DatabaseApplication'], WorkspaceCreateApplicationResponse400, WorkspaceCreateApplicationResponse404]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ApplicationCreate,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    """Creates a new application based on the provided type. The newly created application is going to be
    added to the workspace related to the provided `workspace_id` parameter. If the authorized user does
    not belong to the workspace an error will be returned.

    Args:
        workspace_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ApplicationCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['BuilderApplication', 'DatabaseApplication'], WorkspaceCreateApplicationResponse400, WorkspaceCreateApplicationResponse404]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    *,
    client: AuthenticatedClient,
    json_body: ApplicationCreate,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["BuilderApplication", "DatabaseApplication"],
        WorkspaceCreateApplicationResponse400,
        WorkspaceCreateApplicationResponse404,
    ]
]:
    """Creates a new application based on the provided type. The newly created application is going to be
    added to the workspace related to the provided `workspace_id` parameter. If the authorized user does
    not belong to the workspace an error will be returned.

    Args:
        workspace_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (ApplicationCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['BuilderApplication', 'DatabaseApplication'], WorkspaceCreateApplicationResponse400, WorkspaceCreateApplicationResponse404]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
