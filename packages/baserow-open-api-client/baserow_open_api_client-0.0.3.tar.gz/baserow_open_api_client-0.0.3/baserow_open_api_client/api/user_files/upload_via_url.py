from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upload_via_url_response_400 import UploadViaUrlResponse400
from ...models.user_file import UserFile
from ...models.user_file_upload_via_url_request import UserFileUploadViaURLRequest
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: UserFileUploadViaURLRequest,
) -> Dict[str, Any]:
    url = "{}/api/user-files/upload-via-url/".format(client.base_url)

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[UploadViaUrlResponse400, UserFile]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserFile.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UploadViaUrlResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[UploadViaUrlResponse400, UserFile]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: UserFileUploadViaURLRequest,
) -> Response[Union[UploadViaUrlResponse400, UserFile]]:
    """Uploads a file to Baserow by downloading it from the provided URL.

    Args:
        json_body (UserFileUploadViaURLRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadViaUrlResponse400, UserFile]]
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


def sync(
    *,
    client: AuthenticatedClient,
    json_body: UserFileUploadViaURLRequest,
) -> Optional[Union[UploadViaUrlResponse400, UserFile]]:
    """Uploads a file to Baserow by downloading it from the provided URL.

    Args:
        json_body (UserFileUploadViaURLRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadViaUrlResponse400, UserFile]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: UserFileUploadViaURLRequest,
) -> Response[Union[UploadViaUrlResponse400, UserFile]]:
    """Uploads a file to Baserow by downloading it from the provided URL.

    Args:
        json_body (UserFileUploadViaURLRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadViaUrlResponse400, UserFile]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: UserFileUploadViaURLRequest,
) -> Optional[Union[UploadViaUrlResponse400, UserFile]]:
    """Uploads a file to Baserow by downloading it from the provided URL.

    Args:
        json_body (UserFileUploadViaURLRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadViaUrlResponse400, UserFile]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
