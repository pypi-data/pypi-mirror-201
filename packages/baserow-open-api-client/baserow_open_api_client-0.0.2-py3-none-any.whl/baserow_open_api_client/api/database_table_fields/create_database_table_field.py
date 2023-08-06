from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.boolean_field_create_field import BooleanFieldCreateField
from ...models.boolean_field_field_serializer_with_related_fields import BooleanFieldFieldSerializerWithRelatedFields
from ...models.create_database_table_field_response_400 import CreateDatabaseTableFieldResponse400
from ...models.create_database_table_field_response_401 import CreateDatabaseTableFieldResponse401
from ...models.create_database_table_field_response_404 import CreateDatabaseTableFieldResponse404
from ...models.created_on_field_create_field import CreatedOnFieldCreateField
from ...models.created_on_field_field_serializer_with_related_fields import (
    CreatedOnFieldFieldSerializerWithRelatedFields,
)
from ...models.date_field_create_field import DateFieldCreateField
from ...models.date_field_field_serializer_with_related_fields import DateFieldFieldSerializerWithRelatedFields
from ...models.email_field_create_field import EmailFieldCreateField
from ...models.email_field_field_serializer_with_related_fields import EmailFieldFieldSerializerWithRelatedFields
from ...models.file_field_create_field import FileFieldCreateField
from ...models.file_field_field_serializer_with_related_fields import FileFieldFieldSerializerWithRelatedFields
from ...models.formula_field_create_field import FormulaFieldCreateField
from ...models.formula_field_field_serializer_with_related_fields import FormulaFieldFieldSerializerWithRelatedFields
from ...models.last_modified_field_create_field import LastModifiedFieldCreateField
from ...models.last_modified_field_field_serializer_with_related_fields import (
    LastModifiedFieldFieldSerializerWithRelatedFields,
)
from ...models.link_row_field_create_field import LinkRowFieldCreateField
from ...models.link_row_field_field_serializer_with_related_fields import LinkRowFieldFieldSerializerWithRelatedFields
from ...models.long_text_field_create_field import LongTextFieldCreateField
from ...models.long_text_field_field_serializer_with_related_fields import LongTextFieldFieldSerializerWithRelatedFields
from ...models.lookup_field_create_field import LookupFieldCreateField
from ...models.lookup_field_field_serializer_with_related_fields import LookupFieldFieldSerializerWithRelatedFields
from ...models.multiple_collaborators_field_create_field import MultipleCollaboratorsFieldCreateField
from ...models.multiple_collaborators_field_field_serializer_with_related_fields import (
    MultipleCollaboratorsFieldFieldSerializerWithRelatedFields,
)
from ...models.multiple_select_field_create_field import MultipleSelectFieldCreateField
from ...models.multiple_select_field_field_serializer_with_related_fields import (
    MultipleSelectFieldFieldSerializerWithRelatedFields,
)
from ...models.number_field_create_field import NumberFieldCreateField
from ...models.number_field_field_serializer_with_related_fields import NumberFieldFieldSerializerWithRelatedFields
from ...models.phone_number_field_create_field import PhoneNumberFieldCreateField
from ...models.phone_number_field_field_serializer_with_related_fields import (
    PhoneNumberFieldFieldSerializerWithRelatedFields,
)
from ...models.rating_field_create_field import RatingFieldCreateField
from ...models.rating_field_field_serializer_with_related_fields import RatingFieldFieldSerializerWithRelatedFields
from ...models.single_select_field_create_field import SingleSelectFieldCreateField
from ...models.single_select_field_field_serializer_with_related_fields import (
    SingleSelectFieldFieldSerializerWithRelatedFields,
)
from ...models.text_field_create_field import TextFieldCreateField
from ...models.text_field_field_serializer_with_related_fields import TextFieldFieldSerializerWithRelatedFields
from ...models.url_field_create_field import URLFieldCreateField
from ...models.url_field_field_serializer_with_related_fields import URLFieldFieldSerializerWithRelatedFields
from ...types import UNSET, Response, Unset


def _get_kwargs(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "BooleanFieldCreateField",
        "CreatedOnFieldCreateField",
        "DateFieldCreateField",
        "EmailFieldCreateField",
        "FileFieldCreateField",
        "FormulaFieldCreateField",
        "LastModifiedFieldCreateField",
        "LinkRowFieldCreateField",
        "LongTextFieldCreateField",
        "LookupFieldCreateField",
        "MultipleCollaboratorsFieldCreateField",
        "MultipleSelectFieldCreateField",
        "NumberFieldCreateField",
        "PhoneNumberFieldCreateField",
        "RatingFieldCreateField",
        "SingleSelectFieldCreateField",
        "TextFieldCreateField",
        "URLFieldCreateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/fields/table/{table_id}/".format(client.base_url, table_id=table_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    json_json_body: Dict[str, Any]

    if isinstance(json_body, TextFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, LongTextFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, URLFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, EmailFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, NumberFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RatingFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, BooleanFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, DateFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, LastModifiedFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, CreatedOnFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, LinkRowFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, FileFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, SingleSelectFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, MultipleSelectFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, PhoneNumberFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, FormulaFieldCreateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, LookupFieldCreateField):
        json_json_body = json_body.to_dict()

    else:
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
) -> Optional[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ],
    ]
]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_0 = (
                    TextFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_1 = (
                    LongTextFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_2 = (
                    URLFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_3 = (
                    EmailFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_4 = (
                    NumberFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_5 = (
                    RatingFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_6 = (
                    BooleanFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_7 = (
                    DateFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_8 = (
                    LastModifiedFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_8
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_9 = (
                    CreatedOnFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_9
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_10 = (
                    LinkRowFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_10
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_11 = (
                    FileFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_11
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_12 = (
                    SingleSelectFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_12
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_13 = (
                    MultipleSelectFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_13
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_14 = (
                    PhoneNumberFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_14
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_15 = (
                    FormulaFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_15
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_field_serializer_with_related_fields_type_16 = (
                    LookupFieldFieldSerializerWithRelatedFields.from_dict(data)
                )

                return componentsschemas_field_field_serializer_with_related_fields_type_16
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_field_field_serializer_with_related_fields_type_17 = (
                MultipleCollaboratorsFieldFieldSerializerWithRelatedFields.from_dict(data)
            )

            return componentsschemas_field_field_serializer_with_related_fields_type_17

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateDatabaseTableFieldResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreateDatabaseTableFieldResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateDatabaseTableFieldResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
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
    json_body: Union[
        "BooleanFieldCreateField",
        "CreatedOnFieldCreateField",
        "DateFieldCreateField",
        "EmailFieldCreateField",
        "FileFieldCreateField",
        "FormulaFieldCreateField",
        "LastModifiedFieldCreateField",
        "LinkRowFieldCreateField",
        "LongTextFieldCreateField",
        "LookupFieldCreateField",
        "MultipleCollaboratorsFieldCreateField",
        "MultipleSelectFieldCreateField",
        "NumberFieldCreateField",
        "PhoneNumberFieldCreateField",
        "RatingFieldCreateField",
        "SingleSelectFieldCreateField",
        "TextFieldCreateField",
        "URLFieldCreateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ],
    ]
]:
    """Creates a new field for the table related to the provided `table_id` parameter if the authorized
    user has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.If creating the field causes other fields to change then the specificinstances of
    those fields will be included in the related fields response key.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['BooleanFieldCreateField', 'CreatedOnFieldCreateField',
            'DateFieldCreateField', 'EmailFieldCreateField', 'FileFieldCreateField',
            'FormulaFieldCreateField', 'LastModifiedFieldCreateField', 'LinkRowFieldCreateField',
            'LongTextFieldCreateField', 'LookupFieldCreateField',
            'MultipleCollaboratorsFieldCreateField', 'MultipleSelectFieldCreateField',
            'NumberFieldCreateField', 'PhoneNumberFieldCreateField', 'RatingFieldCreateField',
            'SingleSelectFieldCreateField', 'TextFieldCreateField', 'URLFieldCreateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableFieldResponse400, CreateDatabaseTableFieldResponse401, CreateDatabaseTableFieldResponse404, Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields']]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
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
    json_body: Union[
        "BooleanFieldCreateField",
        "CreatedOnFieldCreateField",
        "DateFieldCreateField",
        "EmailFieldCreateField",
        "FileFieldCreateField",
        "FormulaFieldCreateField",
        "LastModifiedFieldCreateField",
        "LinkRowFieldCreateField",
        "LongTextFieldCreateField",
        "LookupFieldCreateField",
        "MultipleCollaboratorsFieldCreateField",
        "MultipleSelectFieldCreateField",
        "NumberFieldCreateField",
        "PhoneNumberFieldCreateField",
        "RatingFieldCreateField",
        "SingleSelectFieldCreateField",
        "TextFieldCreateField",
        "URLFieldCreateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ],
    ]
]:
    """Creates a new field for the table related to the provided `table_id` parameter if the authorized
    user has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.If creating the field causes other fields to change then the specificinstances of
    those fields will be included in the related fields response key.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['BooleanFieldCreateField', 'CreatedOnFieldCreateField',
            'DateFieldCreateField', 'EmailFieldCreateField', 'FileFieldCreateField',
            'FormulaFieldCreateField', 'LastModifiedFieldCreateField', 'LinkRowFieldCreateField',
            'LongTextFieldCreateField', 'LookupFieldCreateField',
            'MultipleCollaboratorsFieldCreateField', 'MultipleSelectFieldCreateField',
            'NumberFieldCreateField', 'PhoneNumberFieldCreateField', 'RatingFieldCreateField',
            'SingleSelectFieldCreateField', 'TextFieldCreateField', 'URLFieldCreateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableFieldResponse400, CreateDatabaseTableFieldResponse401, CreateDatabaseTableFieldResponse404, Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields']]
    """

    return sync_detailed(
        table_id=table_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "BooleanFieldCreateField",
        "CreatedOnFieldCreateField",
        "DateFieldCreateField",
        "EmailFieldCreateField",
        "FileFieldCreateField",
        "FormulaFieldCreateField",
        "LastModifiedFieldCreateField",
        "LinkRowFieldCreateField",
        "LongTextFieldCreateField",
        "LookupFieldCreateField",
        "MultipleCollaboratorsFieldCreateField",
        "MultipleSelectFieldCreateField",
        "NumberFieldCreateField",
        "PhoneNumberFieldCreateField",
        "RatingFieldCreateField",
        "SingleSelectFieldCreateField",
        "TextFieldCreateField",
        "URLFieldCreateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ],
    ]
]:
    """Creates a new field for the table related to the provided `table_id` parameter if the authorized
    user has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.If creating the field causes other fields to change then the specificinstances of
    those fields will be included in the related fields response key.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['BooleanFieldCreateField', 'CreatedOnFieldCreateField',
            'DateFieldCreateField', 'EmailFieldCreateField', 'FileFieldCreateField',
            'FormulaFieldCreateField', 'LastModifiedFieldCreateField', 'LinkRowFieldCreateField',
            'LongTextFieldCreateField', 'LookupFieldCreateField',
            'MultipleCollaboratorsFieldCreateField', 'MultipleSelectFieldCreateField',
            'NumberFieldCreateField', 'PhoneNumberFieldCreateField', 'RatingFieldCreateField',
            'SingleSelectFieldCreateField', 'TextFieldCreateField', 'URLFieldCreateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateDatabaseTableFieldResponse400, CreateDatabaseTableFieldResponse401, CreateDatabaseTableFieldResponse404, Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields']]]
    """

    kwargs = _get_kwargs(
        table_id=table_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    table_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "BooleanFieldCreateField",
        "CreatedOnFieldCreateField",
        "DateFieldCreateField",
        "EmailFieldCreateField",
        "FileFieldCreateField",
        "FormulaFieldCreateField",
        "LastModifiedFieldCreateField",
        "LinkRowFieldCreateField",
        "LongTextFieldCreateField",
        "LookupFieldCreateField",
        "MultipleCollaboratorsFieldCreateField",
        "MultipleSelectFieldCreateField",
        "NumberFieldCreateField",
        "PhoneNumberFieldCreateField",
        "RatingFieldCreateField",
        "SingleSelectFieldCreateField",
        "TextFieldCreateField",
        "URLFieldCreateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        CreateDatabaseTableFieldResponse400,
        CreateDatabaseTableFieldResponse401,
        CreateDatabaseTableFieldResponse404,
        Union[
            "BooleanFieldFieldSerializerWithRelatedFields",
            "CreatedOnFieldFieldSerializerWithRelatedFields",
            "DateFieldFieldSerializerWithRelatedFields",
            "EmailFieldFieldSerializerWithRelatedFields",
            "FileFieldFieldSerializerWithRelatedFields",
            "FormulaFieldFieldSerializerWithRelatedFields",
            "LastModifiedFieldFieldSerializerWithRelatedFields",
            "LinkRowFieldFieldSerializerWithRelatedFields",
            "LongTextFieldFieldSerializerWithRelatedFields",
            "LookupFieldFieldSerializerWithRelatedFields",
            "MultipleCollaboratorsFieldFieldSerializerWithRelatedFields",
            "MultipleSelectFieldFieldSerializerWithRelatedFields",
            "NumberFieldFieldSerializerWithRelatedFields",
            "PhoneNumberFieldFieldSerializerWithRelatedFields",
            "RatingFieldFieldSerializerWithRelatedFields",
            "SingleSelectFieldFieldSerializerWithRelatedFields",
            "TextFieldFieldSerializerWithRelatedFields",
            "URLFieldFieldSerializerWithRelatedFields",
        ],
    ]
]:
    """Creates a new field for the table related to the provided `table_id` parameter if the authorized
    user has access to the related database's workspace. Depending on the type, different properties can
    optionally be set.If creating the field causes other fields to change then the specificinstances of
    those fields will be included in the related fields response key.

    Args:
        table_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['BooleanFieldCreateField', 'CreatedOnFieldCreateField',
            'DateFieldCreateField', 'EmailFieldCreateField', 'FileFieldCreateField',
            'FormulaFieldCreateField', 'LastModifiedFieldCreateField', 'LinkRowFieldCreateField',
            'LongTextFieldCreateField', 'LookupFieldCreateField',
            'MultipleCollaboratorsFieldCreateField', 'MultipleSelectFieldCreateField',
            'NumberFieldCreateField', 'PhoneNumberFieldCreateField', 'RatingFieldCreateField',
            'SingleSelectFieldCreateField', 'TextFieldCreateField', 'URLFieldCreateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateDatabaseTableFieldResponse400, CreateDatabaseTableFieldResponse401, CreateDatabaseTableFieldResponse404, Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields']]
    """

    return (
        await asyncio_detailed(
            table_id=table_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
