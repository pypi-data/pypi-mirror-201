from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_database_field_unique_row_values_response_400 import GetDatabaseFieldUniqueRowValuesResponse400
from ...models.get_database_field_unique_row_values_response_404 import GetDatabaseFieldUniqueRowValuesResponse404
from ...models.unique_row_values import UniqueRowValues
from ...types import UNSET, Response, Unset


def _get_kwargs(
    field_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    split_comma_separated: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/fields/{field_id}/unique_row_values/".format(client.base_url, field_id=field_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["split_comma_separated"] = split_comma_separated

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
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UniqueRowValues.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetDatabaseFieldUniqueRowValuesResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetDatabaseFieldUniqueRowValuesResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    split_comma_separated: Union[Unset, None, bool] = UNSET,
) -> Response[
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    """Returns a list of all the unique row values for an existing field, sorted in order of frequency.

    Args:
        field_id (int):
        limit (Union[Unset, None, int]):
        split_comma_separated (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
        client=client,
        limit=limit,
        split_comma_separated=split_comma_separated,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    field_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    split_comma_separated: Union[Unset, None, bool] = UNSET,
) -> Optional[
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    """Returns a list of all the unique row values for an existing field, sorted in order of frequency.

    Args:
        field_id (int):
        limit (Union[Unset, None, int]):
        split_comma_separated (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
    """

    return sync_detailed(
        field_id=field_id,
        client=client,
        limit=limit,
        split_comma_separated=split_comma_separated,
    ).parsed


async def asyncio_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    split_comma_separated: Union[Unset, None, bool] = UNSET,
) -> Response[
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    """Returns a list of all the unique row values for an existing field, sorted in order of frequency.

    Args:
        field_id (int):
        limit (Union[Unset, None, int]):
        split_comma_separated (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
        client=client,
        limit=limit,
        split_comma_separated=split_comma_separated,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    field_id: int,
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = UNSET,
    split_comma_separated: Union[Unset, None, bool] = UNSET,
) -> Optional[
    Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
]:
    """Returns a list of all the unique row values for an existing field, sorted in order of frequency.

    Args:
        field_id (int):
        limit (Union[Unset, None, int]):
        split_comma_separated (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetDatabaseFieldUniqueRowValuesResponse400, GetDatabaseFieldUniqueRowValuesResponse404, UniqueRowValues]
    """

    return (
        await asyncio_detailed(
            field_id=field_id,
            client=client,
            limit=limit,
            split_comma_separated=split_comma_separated,
        )
    ).parsed
