from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_builder_page_response_400 import CreateBuilderPageResponse400
from ...models.create_builder_page_response_404 import CreateBuilderPageResponse404
from ...models.create_page import CreatePage
from ...models.page import Page
from ...types import UNSET, Response, Unset


def _get_kwargs(
    builder_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/builder/{builder_id}/pages/".format(client.base_url, builder_id=builder_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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
) -> Optional[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Page.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateBuilderPageResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateBuilderPageResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    builder_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    """Creates a new page for an application builder

    Args:
        builder_id (int):
        client_session_id (Union[Unset, str]):
        json_body (CreatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]
    """

    kwargs = _get_kwargs(
        builder_id=builder_id,
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
    builder_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    """Creates a new page for an application builder

    Args:
        builder_id (int):
        client_session_id (Union[Unset, str]):
        json_body (CreatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]
    """

    return sync_detailed(
        builder_id=builder_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    builder_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    """Creates a new page for an application builder

    Args:
        builder_id (int):
        client_session_id (Union[Unset, str]):
        json_body (CreatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]
    """

    kwargs = _get_kwargs(
        builder_id=builder_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    builder_id: int,
    *,
    client: AuthenticatedClient,
    json_body: CreatePage,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]]:
    """Creates a new page for an application builder

    Args:
        builder_id (int):
        client_session_id (Union[Unset, str]):
        json_body (CreatePage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBuilderPageResponse400, CreateBuilderPageResponse404, Page]
    """

    return (
        await asyncio_detailed(
            builder_id=builder_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
