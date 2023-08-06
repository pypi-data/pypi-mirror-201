from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_database_table_view_decoration_response_400 import CreateDatabaseTableViewDecorationResponse400
from ...models.create_database_table_view_decoration_response_404 import CreateDatabaseTableViewDecorationResponse404
from ...models.generated_conditional_color_create_view_decoration import GeneratedConditionalColorCreateViewDecoration
from ...models.generated_conditional_color_view_decoration import GeneratedConditionalColorViewDecoration
from ...models.generated_single_select_color_create_view_decoration import (
    GeneratedSingleSelectColorCreateViewDecoration,
)
from ...models.generated_single_select_color_view_decoration import GeneratedSingleSelectColorViewDecoration
from ...types import UNSET, Response, Unset


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["GeneratedConditionalColorCreateViewDecoration", "GeneratedSingleSelectColorCreateViewDecoration"],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{view_id}/decorations/".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    json_json_body: Dict[str, Any]

    if isinstance(json_body, GeneratedSingleSelectColorCreateViewDecoration):
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
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_decorator_value_provider_type_view_decoration_type_0 = (
                    GeneratedSingleSelectColorViewDecoration.from_dict(data)
                )

                return componentsschemas_decorator_value_provider_type_view_decoration_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_decorator_value_provider_type_view_decoration_type_1 = (
                GeneratedConditionalColorViewDecoration.from_dict(data)
            )

            return componentsschemas_decorator_value_provider_type_view_decoration_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableViewDecorationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableViewDecorationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
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
    json_body: Union["GeneratedConditionalColorCreateViewDecoration", "GeneratedSingleSelectColorCreateViewDecoration"],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
    ]
]:
    """Creates a new decoration for the view related to the provided `view_id` parameter if the authorized
    user has access to the related database's workspace.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['GeneratedConditionalColorCreateViewDecoration',
            'GeneratedSingleSelectColorCreateViewDecoration']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewDecorationResponse400, CreateDatabaseTableViewDecorationResponse404, Union['GeneratedConditionalColorViewDecoration', 'GeneratedSingleSelectColorViewDecoration']]]
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
    json_body: Union["GeneratedConditionalColorCreateViewDecoration", "GeneratedSingleSelectColorCreateViewDecoration"],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
    ]
]:
    """Creates a new decoration for the view related to the provided `view_id` parameter if the authorized
    user has access to the related database's workspace.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['GeneratedConditionalColorCreateViewDecoration',
            'GeneratedSingleSelectColorCreateViewDecoration']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewDecorationResponse400, CreateDatabaseTableViewDecorationResponse404, Union['GeneratedConditionalColorViewDecoration', 'GeneratedSingleSelectColorViewDecoration']]
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
    json_body: Union["GeneratedConditionalColorCreateViewDecoration", "GeneratedSingleSelectColorCreateViewDecoration"],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
    ]
]:
    """Creates a new decoration for the view related to the provided `view_id` parameter if the authorized
    user has access to the related database's workspace.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['GeneratedConditionalColorCreateViewDecoration',
            'GeneratedSingleSelectColorCreateViewDecoration']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableViewDecorationResponse400, CreateDatabaseTableViewDecorationResponse404, Union['GeneratedConditionalColorViewDecoration', 'GeneratedSingleSelectColorViewDecoration']]]
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
    json_body: Union["GeneratedConditionalColorCreateViewDecoration", "GeneratedSingleSelectColorCreateViewDecoration"],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableViewDecorationResponse400,
        CreateDatabaseTableViewDecorationResponse404,
        Union["GeneratedConditionalColorViewDecoration", "GeneratedSingleSelectColorViewDecoration"],
    ]
]:
    """Creates a new decoration for the view related to the provided `view_id` parameter if the authorized
    user has access to the related database's workspace.

    Args:
        view_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['GeneratedConditionalColorCreateViewDecoration',
            'GeneratedSingleSelectColorCreateViewDecoration']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableViewDecorationResponse400, CreateDatabaseTableViewDecorationResponse404, Union['GeneratedConditionalColorViewDecoration', 'GeneratedSingleSelectColorViewDecoration']]
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
