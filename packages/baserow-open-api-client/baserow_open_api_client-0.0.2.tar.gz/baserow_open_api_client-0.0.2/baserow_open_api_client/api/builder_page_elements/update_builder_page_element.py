from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.heading_element_element import HeadingElementElement
from ...models.heading_element_update_element import HeadingElementUpdateElement
from ...models.paragraph_element_element import ParagraphElementElement
from ...models.paragraph_element_update_element import ParagraphElementUpdateElement
from ...models.update_builder_page_element_response_400 import UpdateBuilderPageElementResponse400
from ...models.update_builder_page_element_response_404 import UpdateBuilderPageElementResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    element_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["HeadingElementUpdateElement", "ParagraphElementUpdateElement"],
    client_session_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/builder/element/{element_id}/".format(client.base_url, element_id=element_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    json_json_body: Dict[str, Any]

    if isinstance(json_body, HeadingElementUpdateElement):
        json_json_body = json_body.to_dict()

    else:
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
) -> Optional[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["HeadingElementElement", "ParagraphElementElement"]:
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

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateBuilderPageElementResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateBuilderPageElementResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
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
    json_body: Union["HeadingElementUpdateElement", "ParagraphElementUpdateElement"],
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
    """Updates an existing builder element.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):
        json_body (Union['HeadingElementUpdateElement', 'ParagraphElementUpdateElement']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['HeadingElementElement', 'ParagraphElementElement'], UpdateBuilderPageElementResponse400, UpdateBuilderPageElementResponse404]]
    """

    kwargs = _get_kwargs(
        element_id=element_id,
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
    element_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["HeadingElementUpdateElement", "ParagraphElementUpdateElement"],
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
    """Updates an existing builder element.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):
        json_body (Union['HeadingElementUpdateElement', 'ParagraphElementUpdateElement']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['HeadingElementElement', 'ParagraphElementElement'], UpdateBuilderPageElementResponse400, UpdateBuilderPageElementResponse404]
    """

    return sync_detailed(
        element_id=element_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    ).parsed


async def asyncio_detailed(
    element_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["HeadingElementUpdateElement", "ParagraphElementUpdateElement"],
    client_session_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
    """Updates an existing builder element.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):
        json_body (Union['HeadingElementUpdateElement', 'ParagraphElementUpdateElement']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['HeadingElementElement', 'ParagraphElementElement'], UpdateBuilderPageElementResponse400, UpdateBuilderPageElementResponse404]]
    """

    kwargs = _get_kwargs(
        element_id=element_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    element_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union["HeadingElementUpdateElement", "ParagraphElementUpdateElement"],
    client_session_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union["HeadingElementElement", "ParagraphElementElement"],
        UpdateBuilderPageElementResponse400,
        UpdateBuilderPageElementResponse404,
    ]
]:
    """Updates an existing builder element.

    Args:
        element_id (int):
        client_session_id (Union[Unset, str]):
        json_body (Union['HeadingElementUpdateElement', 'ParagraphElementUpdateElement']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['HeadingElementElement', 'ParagraphElementElement'], UpdateBuilderPageElementResponse400, UpdateBuilderPageElementResponse404]
    """

    return (
        await asyncio_detailed(
            element_id=element_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
        )
    ).parsed
