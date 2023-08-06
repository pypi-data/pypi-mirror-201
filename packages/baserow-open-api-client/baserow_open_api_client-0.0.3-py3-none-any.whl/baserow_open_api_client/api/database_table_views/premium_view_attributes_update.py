from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_update_premium_view_attributes import PatchedUpdatePremiumViewAttributes
from ...models.premium_view_attributes_update_response_400 import PremiumViewAttributesUpdateResponse400
from ...models.premium_view_attributes_update_response_404 import PremiumViewAttributesUpdateResponse404
from ...models.view import View
from ...types import Response


def _get_kwargs(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePremiumViewAttributes,
) -> Dict[str, Any]:
    url = "{}/api/database/view/{view_id}/premium".format(client.base_url, view_id=view_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

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
) -> Optional[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = View.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PremiumViewAttributesUpdateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = PremiumViewAttributesUpdateResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePremiumViewAttributes,
) -> Response[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    """Sets view attributes only available for premium users.

    Args:
        view_id (int):
        json_body (PatchedUpdatePremiumViewAttributes):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePremiumViewAttributes,
) -> Optional[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    """Sets view attributes only available for premium users.

    Args:
        view_id (int):
        json_body (PatchedUpdatePremiumViewAttributes):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]
    """

    return sync_detailed(
        view_id=view_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePremiumViewAttributes,
) -> Response[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    """Sets view attributes only available for premium users.

    Args:
        view_id (int):
        json_body (PatchedUpdatePremiumViewAttributes):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]
    """

    kwargs = _get_kwargs(
        view_id=view_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    view_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUpdatePremiumViewAttributes,
) -> Optional[Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]]:
    """Sets view attributes only available for premium users.

    Args:
        view_id (int):
        json_body (PatchedUpdatePremiumViewAttributes):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PremiumViewAttributesUpdateResponse400, PremiumViewAttributesUpdateResponse404, View]
    """

    return (
        await asyncio_detailed(
            view_id=view_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
