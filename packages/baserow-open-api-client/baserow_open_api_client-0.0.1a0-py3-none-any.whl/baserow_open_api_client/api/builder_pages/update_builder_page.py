from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.page import Page
from ...models.patched_update_page import PatchedUpdatePage
from ...models.update_builder_page_response_400 import UpdateBuilderPageResponse400
from ...models.update_builder_page_response_404 import UpdateBuilderPageResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    page_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/builder/pages/{page_id}/".format(client.base_url, page_id=page_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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
) -> Optional[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Page.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateBuilderPageResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateBuilderPageResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    page_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    """Updates an existing page of an application builder

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):
        json_body (PatchedUpdatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    page_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    """Updates an existing page of an application builder

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):
        json_body (PatchedUpdatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]
    """

    return sync_detailed(
        page_id=page_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    page_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    """Updates an existing page of an application builder

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):
        json_body (PatchedUpdatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    page_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]]:
    """Updates an existing page of an application builder

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):
        json_body (PatchedUpdatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Page, UpdateBuilderPageResponse400, UpdateBuilderPageResponse404]
    """

    return (
        await asyncio_detailed(
            page_id=page_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
