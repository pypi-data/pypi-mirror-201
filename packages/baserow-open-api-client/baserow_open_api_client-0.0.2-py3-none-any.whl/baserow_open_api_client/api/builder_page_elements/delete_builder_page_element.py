from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_builder_page_element_response_400 import DeleteBuilderPageElementResponse400
from ...models.delete_builder_page_element_response_404 import DeleteBuilderPageElementResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    element_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/builder/element/{element_id}/".format(client.base_url, element_id=element_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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
) -> Optional[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DeleteBuilderPageElementResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteBuilderPageElementResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    element_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    """Deletes the element related by the given id.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]
    """

    kwargs = _get_kwargs(
        element_id=element_id,
        client=client,
        client_session_id=client_session_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    element_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    """Deletes the element related by the given id.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]
    """

    return sync_detailed(
        element_id=element_id,
        client=client,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    element_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    """Deletes the element related by the given id.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]
    """

    kwargs = _get_kwargs(
        element_id=element_id,
        client=client,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    element_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]]:
    """Deletes the element related by the given id.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteBuilderPageElementResponse400, DeleteBuilderPageElementResponse404]
    """

    return (
        await asyncio_detailed(
            element_id=element_id,
            client=client,
            client_session_id=client_session_id,
        )
    ).parsed
