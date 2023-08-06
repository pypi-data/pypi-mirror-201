from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.heading_element_element import HeadingElementElement
from ...models.list_builder_page_elements_response_404 import ListBuilderPageElementsResponse404
from ...models.paragraph_element_element import ParagraphElementElement
from ...types import Response


def _get_kwargs(
    page_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/builder/page/{page_id}/elements/".format(client.base_url, page_id=page_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "get",
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
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> Union["HeadingElementElement", "ParagraphElementElement"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_element_type_element_type_0 = HeadingElementElement.from_dict(data)

                    return componentsschemas_element_type_element_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_element_type_element_type_1 = ParagraphElementElement.from_dict(data)

                return componentsschemas_element_type_element_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListBuilderPageElementsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
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
) -> Response[
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
]:
    """Lists all the elements of the page related to the provided parameter if the user has access to the
    related builder's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible.

    Args:
        page_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListBuilderPageElementsResponse404, List[Union['HeadingElementElement', 'ParagraphElementElement']]]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
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
) -> Optional[
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
]:
    """Lists all the elements of the page related to the provided parameter if the user has access to the
    related builder's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible.

    Args:
        page_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListBuilderPageElementsResponse404, List[Union['HeadingElementElement', 'ParagraphElementElement']]]
    """

    return sync_detailed(
        page_id=page_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    page_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
]:
    """Lists all the elements of the page related to the provided parameter if the user has access to the
    related builder's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible.

    Args:
        page_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListBuilderPageElementsResponse404, List[Union['HeadingElementElement', 'ParagraphElementElement']]]]
    """

    kwargs = _get_kwargs(
        page_id=page_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    page_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[ListBuilderPageElementsResponse404, List[Union["HeadingElementElement", "ParagraphElementElement"]]]
]:
    """Lists all the elements of the page related to the provided parameter if the user has access to the
    related builder's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible.

    Args:
        page_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListBuilderPageElementsResponse404, List[Union['HeadingElementElement', 'ParagraphElementElement']]]
    """

    return (
        await asyncio_detailed(
            page_id=page_id,
            client=client,
        )
    ).parsed
