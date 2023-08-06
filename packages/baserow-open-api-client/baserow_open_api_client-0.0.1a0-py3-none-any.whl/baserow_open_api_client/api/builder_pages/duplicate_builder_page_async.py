from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_builder_page_async_response_400 import DuplicateBuilderPageAsyncResponse400
from ...models.duplicate_builder_page_async_response_404 import DuplicateBuilderPageAsyncResponse404
from ...models.single_duplicate_page_job_type import SingleDuplicatePageJobType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    page_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/builder/pages/{page_id}/duplicate/async/".format(client.base_url, page_id=page_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

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
) -> Optional[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = SingleDuplicatePageJobType.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = DuplicateBuilderPageAsyncResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DuplicateBuilderPageAsyncResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
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
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
    """Start a job to duplicate the page with the provided `page_id` parameter if the authorized user has
    access to the builder's workspace.

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
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
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
    """Start a job to duplicate the page with the provided `page_id` parameter if the authorized user has
    access to the builder's workspace.

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
    """

    return sync_detailed(
        page_id=page_id,
        client=client,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    page_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
    """Start a job to duplicate the page with the provided `page_id` parameter if the authorized user has
    access to the builder's workspace.

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    page_id: int,
    *,
    client: AuthenticatedClient,
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
]:
    """Start a job to duplicate the page with the provided `page_id` parameter if the authorized user has
    access to the builder's workspace.

    Args:
        page_id (int):
        client_session_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DuplicateBuilderPageAsyncResponse400, DuplicateBuilderPageAsyncResponse404, SingleDuplicatePageJobType]
    """

    return (
        await asyncio_detailed(
            page_id=page_id,
            client=client,
            client_session_id=client_session_id,
        )
    ).parsed
