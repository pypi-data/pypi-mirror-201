from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_edit_user_response_400 import AdminEditUserResponse400
from ...models.patched_user_admin_update import PatchedUserAdminUpdate
from ...models.user_admin_response import UserAdminResponse
from ...types import Response


def _get_kwargs(
    user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUserAdminUpdate,
) -> Dict[str, Any]:
    url = "{}/api/admin/users/{user_id}/".format(client.base_url, user_id=user_id)

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
) -> Optional[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserAdminResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AdminEditUserResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUserAdminUpdate,
) -> Response[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    """Updates specified user attributes and returns the updated user if the requesting user is staff. You
    cannot update yourself to no longer be an admin or active.

    This is a **premium** feature.

    Args:
        user_id (int):
        json_body (PatchedUserAdminUpdate): Serializes a request body for updating a given user.
            Do not use for returning user
            data as the password will be returned also.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminEditUserResponse400, Any, UserAdminResponse]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUserAdminUpdate,
) -> Optional[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    """Updates specified user attributes and returns the updated user if the requesting user is staff. You
    cannot update yourself to no longer be an admin or active.

    This is a **premium** feature.

    Args:
        user_id (int):
        json_body (PatchedUserAdminUpdate): Serializes a request body for updating a given user.
            Do not use for returning user
            data as the password will be returned also.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminEditUserResponse400, Any, UserAdminResponse]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUserAdminUpdate,
) -> Response[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    """Updates specified user attributes and returns the updated user if the requesting user is staff. You
    cannot update yourself to no longer be an admin or active.

    This is a **premium** feature.

    Args:
        user_id (int):
        json_body (PatchedUserAdminUpdate): Serializes a request body for updating a given user.
            Do not use for returning user
            data as the password will be returned also.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AdminEditUserResponse400, Any, UserAdminResponse]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: int,
    *,
    client: AuthenticatedClient,
    json_body: PatchedUserAdminUpdate,
) -> Optional[Union[AdminEditUserResponse400, Any, UserAdminResponse]]:
    """Updates specified user attributes and returns the updated user if the requesting user is staff. You
    cannot update yourself to no longer be an admin or active.

    This is a **premium** feature.

    Args:
        user_id (int):
        json_body (PatchedUserAdminUpdate): Serializes a request body for updating a given user.
            Do not use for returning user
            data as the password will be returned also.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AdminEditUserResponse400, Any, UserAdminResponse]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
