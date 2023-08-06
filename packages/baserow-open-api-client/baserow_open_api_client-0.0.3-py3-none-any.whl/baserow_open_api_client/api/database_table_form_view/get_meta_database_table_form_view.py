from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_meta_database_table_form_view_response_401 import GetMetaDatabaseTableFormViewResponse401
from ...models.get_meta_database_table_form_view_response_404 import GetMetaDatabaseTableFormViewResponse404
from ...models.public_form_view import PublicFormView
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/form/{slug}/submit/".format(client.base_url, slug=slug)

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
) -> Optional[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PublicFormView.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetMetaDatabaseTableFormViewResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetMetaDatabaseTableFormViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
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
) -> Response[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
    """Returns the meta data related to the form view if the form is publicly shared or if the user has
    access to the related workspace. This data can be used to construct a form with the right fields.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
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
) -> Optional[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
    """Returns the meta data related to the form view if the form is publicly shared or if the user has
    access to the related workspace. This data can be used to construct a form with the right fields.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]
    """

    return sync_detailed(
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
    """Returns the meta data related to the form view if the form is publicly shared or if the user has
    access to the related workspace. This data can be used to construct a form with the right fields.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]]:
    """Returns the meta data related to the form view if the form is publicly shared or if the user has
    access to the related workspace. This data can be used to construct a form with the right fields.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetMetaDatabaseTableFormViewResponse401, GetMetaDatabaseTableFormViewResponse404, PublicFormView]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
        )
    ).parsed
