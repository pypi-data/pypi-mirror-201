from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.type_formula_field_response_400 import TypeFormulaFieldResponse400
from ...models.type_formula_field_response_404 import TypeFormulaFieldResponse404
from ...models.type_formula_request import TypeFormulaRequest
from ...models.type_formula_result import TypeFormulaResult
from ...types import Response


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TypeFormulaRequest,
) -> Dict[str, Any]:
    url = "{}/api/database/formula/{table_id}/type/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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
) -> Optional[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TypeFormulaResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = TypeFormulaFieldResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = TypeFormulaFieldResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TypeFormulaRequest,
) -> Response[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    """Calculates and returns the type of the specified formula value. Does not change the state of the
    field in any way.

    Args:
        table_id (int):
        json_body (TypeFormulaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TypeFormulaRequest,
) -> Optional[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    """Calculates and returns the type of the specified formula value. Does not change the state of the
    field in any way.

    Args:
        table_id (int):
        json_body (TypeFormulaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TypeFormulaRequest,
) -> Response[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    """Calculates and returns the type of the specified formula value. Does not change the state of the
    field in any way.

    Args:
        table_id (int):
        json_body (TypeFormulaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: TypeFormulaRequest,
) -> Optional[Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]]:
    """Calculates and returns the type of the specified formula value. Does not change the state of the
    field in any way.

    Args:
        table_id (int):
        json_body (TypeFormulaRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[TypeFormulaFieldResponse400, TypeFormulaFieldResponse404, TypeFormulaResult]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
