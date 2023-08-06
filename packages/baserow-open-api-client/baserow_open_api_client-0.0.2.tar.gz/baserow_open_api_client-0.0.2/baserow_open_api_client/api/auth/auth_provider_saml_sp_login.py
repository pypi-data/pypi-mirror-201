from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/sso/saml/login/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["email"] = email

    params["group_invitation_token"] = group_invitation_token

    params["language"] = language

    params["original"] = original

    params["workspace_invitation_token"] = workspace_invitation_token

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
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """This is the endpoint that is called when the user wants to initiate a SSO SAML login from Baserow
    (the service provider). The user will be redirected to the SAML identity provider (IdP) where the
    user can authenticate. Once logged in in the IdP, the user will be redirected back to the assertion
    consumer service endpoint (ACS) where the SAML response will be validated and a new JWT session
    token will be provided to work with Baserow APIs.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        email=email,
        group_invitation_token=group_invitation_token,
        language=language,
        original=original,
        workspace_invitation_token=workspace_invitation_token,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
    group_invitation_token: Union[Unset, None, str] = UNSET,
    language: Union[Unset, None, str] = UNSET,
    original: Union[Unset, None, str] = UNSET,
    workspace_invitation_token: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """This is the endpoint that is called when the user wants to initiate a SSO SAML login from Baserow
    (the service provider). The user will be redirected to the SAML identity provider (IdP) where the
    user can authenticate. Once logged in in the IdP, the user will be redirected back to the assertion
    consumer service endpoint (ACS) where the SAML response will be validated and a new JWT session
    token will be provided to work with Baserow APIs.

    Args:
        email (Union[Unset, None, str]):
        group_invitation_token (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        original (Union[Unset, None, str]):
        workspace_invitation_token (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        email=email,
        group_invitation_token=group_invitation_token,
        language=language,
        original=original,
        workspace_invitation_token=workspace_invitation_token,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
