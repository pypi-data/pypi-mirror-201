from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_database_table_row_names_response_200 import ListDatabaseTableRowNamesResponse200
from ...models.list_database_table_row_names_response_400 import ListDatabaseTableRowNamesResponse400
from ...models.list_database_table_row_names_response_401 import ListDatabaseTableRowNamesResponse401
from ...models.list_database_table_row_names_response_404 import ListDatabaseTableRowNamesResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    table_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/rows/names/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["table__{id}"] = table_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    result = {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }

    if hasattr(client, "auth"):
        result["auth"] = client.auth

    return result


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListDatabaseTableRowNamesResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableRowNamesResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListDatabaseTableRowNamesResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableRowNamesResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    table_id: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    """Returns the names of the given row of the given tables. The nameof a row is the primary field value
    for this row. The result can be usedfor example, when you want to display the name of a linked row
    from another table.

    Args:
        table_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableRowNamesResponse200, ListDatabaseTableRowNamesResponse400, ListDatabaseTableRowNamesResponse401, ListDatabaseTableRowNamesResponse404]]
    """

    kwargs = _get_kwargs(
        client=client,
        table_id=table_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    table_id: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    """Returns the names of the given row of the given tables. The nameof a row is the primary field value
    for this row. The result can be usedfor example, when you want to display the name of a linked row
    from another table.

    Args:
        table_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableRowNamesResponse200, ListDatabaseTableRowNamesResponse400, ListDatabaseTableRowNamesResponse401, ListDatabaseTableRowNamesResponse404]
    """

    return sync_detailed(
        client=client,
        table_id=table_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    table_id: Union[Unset, None, str] = UNSET,
) -> Response[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    """Returns the names of the given row of the given tables. The nameof a row is the primary field value
    for this row. The result can be usedfor example, when you want to display the name of a linked row
    from another table.

    Args:
        table_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableRowNamesResponse200, ListDatabaseTableRowNamesResponse400, ListDatabaseTableRowNamesResponse401, ListDatabaseTableRowNamesResponse404]]
    """

    kwargs = _get_kwargs(
        client=client,
        table_id=table_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    table_id: Union[Unset, None, str] = UNSET,
) -> Optional[
    Union[
        ListDatabaseTableRowNamesResponse200,
        ListDatabaseTableRowNamesResponse400,
        ListDatabaseTableRowNamesResponse401,
        ListDatabaseTableRowNamesResponse404,
    ]
]:
    """Returns the names of the given row of the given tables. The nameof a row is the primary field value
    for this row. The result can be usedfor example, when you want to display the name of a linked row
    from another table.

    Args:
        table_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableRowNamesResponse200, ListDatabaseTableRowNamesResponse400, ListDatabaseTableRowNamesResponse401, ListDatabaseTableRowNamesResponse404]
    """

    return (
        await asyncio_detailed(
            client=client,
            table_id=table_id,
        )
    ).parsed
