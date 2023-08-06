from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.boolean_field_field import BooleanFieldField
from ...models.created_on_field_field import CreatedOnFieldField
from ...models.date_field_field import DateFieldField
from ...models.email_field_field import EmailFieldField
from ...models.file_field_field import FileFieldField
from ...models.formula_field_field import FormulaFieldField
from ...models.last_modified_field_field import LastModifiedFieldField
from ...models.link_row_field_field import LinkRowFieldField
from ...models.list_database_table_fields_response_400 import ListDatabaseTableFieldsResponse400
from ...models.list_database_table_fields_response_401 import ListDatabaseTableFieldsResponse401
from ...models.list_database_table_fields_response_404 import ListDatabaseTableFieldsResponse404
from ...models.long_text_field_field import LongTextFieldField
from ...models.lookup_field_field import LookupFieldField
from ...models.multiple_collaborators_field_field import MultipleCollaboratorsFieldField
from ...models.multiple_select_field_field import MultipleSelectFieldField
from ...models.number_field_field import NumberFieldField
from ...models.phone_number_field_field import PhoneNumberFieldField
from ...models.rating_field_field import RatingFieldField
from ...models.single_select_field_field import SingleSelectFieldField
from ...models.text_field_field import TextFieldField
from ...models.url_field_field import URLFieldField
from ...types import Response


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/database/fields/table/{table_id}/".format(client.base_url, table_id=table_id)

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
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_0 = TextFieldField.from_dict(data)

                    return componentsschemas_field_field_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_1 = LongTextFieldField.from_dict(data)

                    return componentsschemas_field_field_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_2 = URLFieldField.from_dict(data)

                    return componentsschemas_field_field_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_3 = EmailFieldField.from_dict(data)

                    return componentsschemas_field_field_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_4 = NumberFieldField.from_dict(data)

                    return componentsschemas_field_field_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_5 = RatingFieldField.from_dict(data)

                    return componentsschemas_field_field_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_6 = BooleanFieldField.from_dict(data)

                    return componentsschemas_field_field_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_7 = DateFieldField.from_dict(data)

                    return componentsschemas_field_field_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_8 = LastModifiedFieldField.from_dict(data)

                    return componentsschemas_field_field_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_9 = CreatedOnFieldField.from_dict(data)

                    return componentsschemas_field_field_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_10 = LinkRowFieldField.from_dict(data)

                    return componentsschemas_field_field_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_11 = FileFieldField.from_dict(data)

                    return componentsschemas_field_field_type_11
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_12 = SingleSelectFieldField.from_dict(data)

                    return componentsschemas_field_field_type_12
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_13 = MultipleSelectFieldField.from_dict(data)

                    return componentsschemas_field_field_type_13
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_14 = PhoneNumberFieldField.from_dict(data)

                    return componentsschemas_field_field_type_14
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_15 = FormulaFieldField.from_dict(data)

                    return componentsschemas_field_field_type_15
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_field_type_16 = LookupFieldField.from_dict(data)

                    return componentsschemas_field_field_type_16
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_type_17 = MultipleCollaboratorsFieldField.from_dict(data)

                return componentsschemas_field_field_type_17

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListDatabaseTableFieldsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ListDatabaseTableFieldsResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListDatabaseTableFieldsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
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
) -> Response[
    Union[
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
    """Lists all the fields of the table related to the provided parameter if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table consists of fields and each field can have a different type. Each type
    can have different properties. A field is comparable with a regular table's column.

    Args:
        table_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableFieldsResponse400, ListDatabaseTableFieldsResponse401, ListDatabaseTableFieldsResponse404, List[Union['BooleanFieldField', 'CreatedOnFieldField', 'DateFieldField', 'EmailFieldField', 'FileFieldField', 'FormulaFieldField', 'LastModifiedFieldField', 'LinkRowFieldField', 'LongTextFieldField', 'LookupFieldField', 'MultipleCollaboratorsFieldField', 'MultipleSelectFieldField', 'NumberFieldField', 'PhoneNumberFieldField', 'RatingFieldField', 'SingleSelectFieldField', 'TextFieldField', 'URLFieldField']]]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
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
) -> Optional[
    Union[
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
    """Lists all the fields of the table related to the provided parameter if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table consists of fields and each field can have a different type. Each type
    can have different properties. A field is comparable with a regular table's column.

    Args:
        table_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableFieldsResponse400, ListDatabaseTableFieldsResponse401, ListDatabaseTableFieldsResponse404, List[Union['BooleanFieldField', 'CreatedOnFieldField', 'DateFieldField', 'EmailFieldField', 'FileFieldField', 'FormulaFieldField', 'LastModifiedFieldField', 'LinkRowFieldField', 'LongTextFieldField', 'LookupFieldField', 'MultipleCollaboratorsFieldField', 'MultipleSelectFieldField', 'NumberFieldField', 'PhoneNumberFieldField', 'RatingFieldField', 'SingleSelectFieldField', 'TextFieldField', 'URLFieldField']]]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
    """Lists all the fields of the table related to the provided parameter if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table consists of fields and each field can have a different type. Each type
    can have different properties. A field is comparable with a regular table's column.

    Args:
        table_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListDatabaseTableFieldsResponse400, ListDatabaseTableFieldsResponse401, ListDatabaseTableFieldsResponse404, List[Union['BooleanFieldField', 'CreatedOnFieldField', 'DateFieldField', 'EmailFieldField', 'FileFieldField', 'FormulaFieldField', 'LastModifiedFieldField', 'LinkRowFieldField', 'LongTextFieldField', 'LookupFieldField', 'MultipleCollaboratorsFieldField', 'MultipleSelectFieldField', 'NumberFieldField', 'PhoneNumberFieldField', 'RatingFieldField', 'SingleSelectFieldField', 'TextFieldField', 'URLFieldField']]]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        ListDatabaseTableFieldsResponse400,
        ListDatabaseTableFieldsResponse401,
        ListDatabaseTableFieldsResponse404,
        List[
            Union[
                "BooleanFieldField",
                "CreatedOnFieldField",
                "DateFieldField",
                "EmailFieldField",
                "FileFieldField",
                "FormulaFieldField",
                "LastModifiedFieldField",
                "LinkRowFieldField",
                "LongTextFieldField",
                "LookupFieldField",
                "MultipleCollaboratorsFieldField",
                "MultipleSelectFieldField",
                "NumberFieldField",
                "PhoneNumberFieldField",
                "RatingFieldField",
                "SingleSelectFieldField",
                "TextFieldField",
                "URLFieldField",
            ]
        ],
    ]
]:
    """Lists all the fields of the table related to the provided parameter if the user has access to the
    related database's workspace. If the workspace is related to a template, then this endpoint will be
    publicly accessible. A table consists of fields and each field can have a different type. Each type
    can have different properties. A field is comparable with a regular table's column.

    Args:
        table_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListDatabaseTableFieldsResponse400, ListDatabaseTableFieldsResponse401, ListDatabaseTableFieldsResponse404, List[Union['BooleanFieldField', 'CreatedOnFieldField', 'DateFieldField', 'EmailFieldField', 'FileFieldField', 'FormulaFieldField', 'LastModifiedFieldField', 'LinkRowFieldField', 'LongTextFieldField', 'LookupFieldField', 'MultipleCollaboratorsFieldField', 'MultipleSelectFieldField', 'NumberFieldField', 'PhoneNumberFieldField', 'RatingFieldField', 'SingleSelectFieldField', 'TextFieldField', 'URLFieldField']]]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
        )
    ).parsed
