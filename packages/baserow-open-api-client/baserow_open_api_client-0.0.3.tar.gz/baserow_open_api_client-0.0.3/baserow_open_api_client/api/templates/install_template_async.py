from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.install_template_async_response_400 import InstallTemplateAsyncResponse400
from ...models.install_template_async_response_404 import InstallTemplateAsyncResponse404
from ...models.single_install_template_job_type import SingleInstallTemplateJobType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: int,
    template_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/templates/install/{workspace_id}/{template_id}/async/".format(
        client.base_url, workspace_id=workspace_id, template_id=template_id
    )

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
) -> Optional[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleInstallTemplateJobType.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = InstallTemplateAsyncResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = InstallTemplateAsyncResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: int,
    template_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    """Start an async job to install the applications of the given template into the given workspace if the
    user has access to that workspace. The response contains those newly created applications.

    Args:
        workspace_id (int):
        template_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        template_id=template_id,
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
    workspace_id: int,
    template_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    """Start an async job to install the applications of the given template into the given workspace if the
    user has access to that workspace. The response contains those newly created applications.

    Args:
        workspace_id (int):
        template_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        template_id=template_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    workspace_id: int,
    template_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    """Start an async job to install the applications of the given template into the given workspace if the
    user has access to that workspace. The response contains those newly created applications.

    Args:
        workspace_id (int):
        template_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        template_id=template_id,
        client=client,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: int,
    template_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]]:
    """Start an async job to install the applications of the given template into the given workspace if the
    user has access to that workspace. The response contains those newly created applications.

    Args:
        workspace_id (int):
        template_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InstallTemplateAsyncResponse400, InstallTemplateAsyncResponse404, SingleInstallTemplateJobType]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            template_id=template_id,
            client=client,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
