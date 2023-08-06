from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.saml_response import SAMLResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: SAMLResponse,
) -> Dict[str, Any]:
    url = "{}/api/sso/saml/acs/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: SAMLResponse,
) -> Response[Any]:
    """Complete the SAML authentication flow by validating the SAML response. Sign in the user if already
    exists in Baserow or create a new one otherwise. Once authenticated, the user will be redirected to
    the original URL they were trying to access. If the response is invalid, the user will be redirected
    to an error page with a specific error message.It accepts the language code and the workspace
    invitation token as query parameters if provided.

    Args:
        json_body (SAMLResponse):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    json_body: SAMLResponse,
) -> Response[Any]:
    """Complete the SAML authentication flow by validating the SAML response. Sign in the user if already
    exists in Baserow or create a new one otherwise. Once authenticated, the user will be redirected to
    the original URL they were trying to access. If the response is invalid, the user will be redirected
    to an error page with a specific error message.It accepts the language code and the workspace
    invitation token as query parameters if provided.

    Args:
        json_body (SAMLResponse):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
