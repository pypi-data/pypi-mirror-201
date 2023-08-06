from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upload_file_form_view_response_400 import UploadFileFormViewResponse400
from ...models.upload_file_form_view_response_401 import UploadFileFormViewResponse401
from ...models.upload_file_form_view_response_404 import UploadFileFormViewResponse404
from ...models.user_file import UserFile
from ...types import Response


def _get_kwargs(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/views/form/{slug}/upload-file/".format(client.base_url, slug=slug)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    result = {
        "method": "post",
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
) -> Optional[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserFile.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UploadFileFormViewResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UploadFileFormViewResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UploadFileFormViewResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
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
) -> Response[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
    """Uploads a file anonymously to Baserow by uploading the file contents directly. A `file` multipart is
    expected containing the file contents.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]]
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
) -> Optional[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
    """Uploads a file anonymously to Baserow by uploading the file contents directly. A `file` multipart is
    expected containing the file contents.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
    """

    return sync_detailed(
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
    """Uploads a file anonymously to Baserow by uploading the file contents directly. A `file` multipart is
    expected containing the file contents.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]]
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
) -> Optional[
    Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
]:
    """Uploads a file anonymously to Baserow by uploading the file contents directly. A `file` multipart is
    expected containing the file contents.

    Args:
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadFileFormViewResponse400, UploadFileFormViewResponse401, UploadFileFormViewResponse404, UserFile]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
        )
    ).parsed
