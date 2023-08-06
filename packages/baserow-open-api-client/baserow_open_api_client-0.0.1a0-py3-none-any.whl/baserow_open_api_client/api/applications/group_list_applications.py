from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.builder_application import BuilderApplication
from ...models.database_application import DatabaseApplication
from ...models.group_list_applications_response_400 import GroupListApplicationsResponse400
from ...models.group_list_applications_response_404 import GroupListApplicationsResponse404
from ...types import Response


def _get_kwargs(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/applications/group/{group_id}/".format(client.base_url, group_id=group_id)

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
) -> Optional[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> Union["BuilderApplication", "DatabaseApplication"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_applications_type_0 = DatabaseApplication.from_dict(data)

                    return componentsschemas_applications_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_applications_type_1 = BuilderApplication.from_dict(data)

                return componentsschemas_applications_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GroupListApplicationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GroupListApplicationsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_applications](#tag/Applications/operation/workspace_list_applications).**

    **Support for this endpoint will end in 2024.**

     Lists all the applications of the group related to the provided `group_id` parameter if the
    authorized user is in that group. If the group is related to a template, then this endpoint will be
    publicly accessible. The properties that belong to the application can differ per type. An
    application always belongs to a single group.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListApplicationsResponse400, GroupListApplicationsResponse404, List[Union['BuilderApplication', 'DatabaseApplication']]]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_applications](#tag/Applications/operation/workspace_list_applications).**

    **Support for this endpoint will end in 2024.**

     Lists all the applications of the group related to the provided `group_id` parameter if the
    authorized user is in that group. If the group is related to a template, then this endpoint will be
    publicly accessible. The properties that belong to the application can differ per type. An
    application always belongs to a single group.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListApplicationsResponse400, GroupListApplicationsResponse404, List[Union['BuilderApplication', 'DatabaseApplication']]]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_applications](#tag/Applications/operation/workspace_list_applications).**

    **Support for this endpoint will end in 2024.**

     Lists all the applications of the group related to the provided `group_id` parameter if the
    authorized user is in that group. If the group is related to a template, then this endpoint will be
    publicly accessible. The properties that belong to the application can differ per type. An
    application always belongs to a single group.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupListApplicationsResponse400, GroupListApplicationsResponse404, List[Union['BuilderApplication', 'DatabaseApplication']]]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        GroupListApplicationsResponse400,
        GroupListApplicationsResponse404,
        List[Union["BuilderApplication", "DatabaseApplication"]],
    ]
]:
    """**This endpoint has been deprecated and replaced with a new endpoint,
    [workspace_list_applications](#tag/Applications/operation/workspace_list_applications).**

    **Support for this endpoint will end in 2024.**

     Lists all the applications of the group related to the provided `group_id` parameter if the
    authorized user is in that group. If the group is related to a template, then this endpoint will be
    publicly accessible. The properties that belong to the application can differ per type. An
    application always belongs to a single group.

    Args:
        group_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupListApplicationsResponse400, GroupListApplicationsResponse404, List[Union['BuilderApplication', 'DatabaseApplication']]]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
        )
    ).parsed
