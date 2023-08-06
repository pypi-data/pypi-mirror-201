from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.database_table_public_view_link_row_field_lookup_response_401 import (
    DatabaseTablePublicViewLinkRowFieldLookupResponse401,
)
from ...models.database_table_public_view_link_row_field_lookup_response_404 import (
    DatabaseTablePublicViewLinkRowFieldLookupResponse404,
)
from ...models.pagination_serializer_link_row_value import PaginationSerializerLinkRowValue
from ...types import Response


def _get_kwargs(
    slug: str,
    field_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/{slug}/link-row-field-lookup/{field_id}/".format(
        client.base_url, slug=slug, field_id=field_id
    )

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
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PaginationSerializerLinkRowValue.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DatabaseTablePublicViewLinkRowFieldLookupResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DatabaseTablePublicViewLinkRowFieldLookupResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    field_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    """If the view is publicly shared or if an authenticated user has access to the related workspace, then
    this endpoint can be used to do a value lookup of the link row fields that are included in the view.
    Normally it is not possible for a not authenticated visitor to fetch the rows of a table. This
    endpoint makes it possible to fetch the id and primary field value of the related table of a link
    row included in the view.

    Args:
        slug (str):
        field_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatabaseTablePublicViewLinkRowFieldLookupResponse401, DatabaseTablePublicViewLinkRowFieldLookupResponse404, PaginationSerializerLinkRowValue]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        field_id=field_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    field_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    """If the view is publicly shared or if an authenticated user has access to the related workspace, then
    this endpoint can be used to do a value lookup of the link row fields that are included in the view.
    Normally it is not possible for a not authenticated visitor to fetch the rows of a table. This
    endpoint makes it possible to fetch the id and primary field value of the related table of a link
    row included in the view.

    Args:
        slug (str):
        field_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatabaseTablePublicViewLinkRowFieldLookupResponse401, DatabaseTablePublicViewLinkRowFieldLookupResponse404, PaginationSerializerLinkRowValue]
    """

    return sync_detailed(
        slug=slug,
        field_id=field_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    slug: str,
    field_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    """If the view is publicly shared or if an authenticated user has access to the related workspace, then
    this endpoint can be used to do a value lookup of the link row fields that are included in the view.
    Normally it is not possible for a not authenticated visitor to fetch the rows of a table. This
    endpoint makes it possible to fetch the id and primary field value of the related table of a link
    row included in the view.

    Args:
        slug (str):
        field_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatabaseTablePublicViewLinkRowFieldLookupResponse401, DatabaseTablePublicViewLinkRowFieldLookupResponse404, PaginationSerializerLinkRowValue]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        field_id=field_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    field_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        DatabaseTablePublicViewLinkRowFieldLookupResponse401,
        DatabaseTablePublicViewLinkRowFieldLookupResponse404,
        PaginationSerializerLinkRowValue,
    ]
]:
    """If the view is publicly shared or if an authenticated user has access to the related workspace, then
    this endpoint can be used to do a value lookup of the link row fields that are included in the view.
    Normally it is not possible for a not authenticated visitor to fetch the rows of a table. This
    endpoint makes it possible to fetch the id and primary field value of the related table of a link
    row included in the view.

    Args:
        slug (str):
        field_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatabaseTablePublicViewLinkRowFieldLookupResponse401, DatabaseTablePublicViewLinkRowFieldLookupResponse404, PaginationSerializerLinkRowValue]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            field_id=field_id,
            client=client,
        )
    ).parsed
