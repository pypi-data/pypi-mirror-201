from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_table_webhook_update_request import PatchedTableWebhookUpdateRequest
from ...models.table_webhook import TableWebhook
from ...models.update_database_table_webhook_response_400 import UpdateDatabaseTableWebhookResponse400
from ...models.update_database_table_webhook_response_404 import UpdateDatabaseTableWebhookResponse404
from ...types import Response


def _get_kwargs(
    webhook_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTableWebhookUpdateRequest,
) -> Dict[str, Any]:
    url = "{}/api/database/webhooks/{webhook_id}/".format(client.base_url, webhook_id=webhook_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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
) -> Optional[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TableWebhook.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateDatabaseTableWebhookResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateDatabaseTableWebhookResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTableWebhookUpdateRequest,
) -> Response[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    """Updates the existing view if the authorized user has access to the related database workspace.

    Args:
        webhook_id (int):
        json_body (PatchedTableWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTableWebhookUpdateRequest,
) -> Optional[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    """Updates the existing view if the authorized user has access to the related database workspace.

    Args:
        webhook_id (int):
        json_body (PatchedTableWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    webhook_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTableWebhookUpdateRequest,
) -> Response[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    """Updates the existing view if the authorized user has access to the related database workspace.

    Args:
        webhook_id (int):
        json_body (PatchedTableWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedTableWebhookUpdateRequest,
) -> Optional[Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]]:
    """Updates the existing view if the authorized user has access to the related database workspace.

    Args:
        webhook_id (int):
        json_body (PatchedTableWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TableWebhook, UpdateDatabaseTableWebhookResponse400, UpdateDatabaseTableWebhookResponse404]
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
