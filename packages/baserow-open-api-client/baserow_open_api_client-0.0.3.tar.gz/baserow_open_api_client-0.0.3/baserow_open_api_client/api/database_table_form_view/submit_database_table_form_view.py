from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.example_row_request import ExampleRowRequest
from ...models.form_view_submitted import FormViewSubmitted
from ...models.submit_database_table_form_view_response_401 import SubmitDatabaseTableFormViewResponse401
from ...models.submit_database_table_form_view_response_404 import SubmitDatabaseTableFormViewResponse404
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequest,
) -> Dict[str, Any]:
    url = "{}/api/database/views/form/{slug}/submit/".format(client.base_url, slug=slug)

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
) -> Optional[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = FormViewSubmitted.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = SubmitDatabaseTableFormViewResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = SubmitDatabaseTableFormViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequest,
) -> Response[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    """Submits the form if the form is publicly shared or if the user has access to the related workspace.
    The provided data will be validated based on the fields that are in the form and the rules per
    field. If valid, a new row will be created in the table.

    Args:
        slug (str):
        json_body (ExampleRowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequest,
) -> Optional[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    """Submits the form if the form is publicly shared or if the user has access to the related workspace.
    The provided data will be validated based on the fields that are in the form and the rules per
    field. If valid, a new row will be created in the table.

    Args:
        slug (str):
        json_body (ExampleRowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]
    """

    return sync_detailed(
        slug=slug,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequest,
) -> Response[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    """Submits the form if the form is publicly shared or if the user has access to the related workspace.
    The provided data will be validated based on the fields that are in the form and the rules per
    field. If valid, a new row will be created in the table.

    Args:
        slug (str):
        json_body (ExampleRowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    json_body: ExampleRowRequest,
) -> Optional[Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]]:
    """Submits the form if the form is publicly shared or if the user has access to the related workspace.
    The provided data will be validated based on the fields that are in the form and the rules per
    field. If valid, a new row will be created in the table.

    Args:
        slug (str):
        json_body (ExampleRowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FormViewSubmitted, SubmitDatabaseTableFormViewResponse401, SubmitDatabaseTableFormViewResponse404]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            json_body=json_body,
        )
    ).parsed
