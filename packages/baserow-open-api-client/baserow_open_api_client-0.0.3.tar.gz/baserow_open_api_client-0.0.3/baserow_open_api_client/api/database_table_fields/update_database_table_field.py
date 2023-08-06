from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.boolean_field_field_serializer_with_related_fields import BooleanFieldFieldSerializerWithRelatedFields
from ...models.created_on_field_field_serializer_with_related_fields import (
    CreatedOnFieldFieldSerializerWithRelatedFields,
)
from ...models.date_field_field_serializer_with_related_fields import DateFieldFieldSerializerWithRelatedFields
from ...models.email_field_field_serializer_with_related_fields import EmailFieldFieldSerializerWithRelatedFields
from ...models.file_field_field_serializer_with_related_fields import FileFieldFieldSerializerWithRelatedFields
from ...models.formula_field_field_serializer_with_related_fields import FormulaFieldFieldSerializerWithRelatedFields
from ...models.last_modified_field_field_serializer_with_related_fields import (
    LastModifiedFieldFieldSerializerWithRelatedFields,
)
from ...models.link_row_field_field_serializer_with_related_fields import LinkRowFieldFieldSerializerWithRelatedFields
from ...models.long_text_field_field_serializer_with_related_fields import LongTextFieldFieldSerializerWithRelatedFields
from ...models.lookup_field_field_serializer_with_related_fields import LookupFieldFieldSerializerWithRelatedFields
from ...models.multiple_collaborators_field_field_serializer_with_related_fields import (
    MultipleCollaboratorsFieldFieldSerializerWithRelatedFields,
)
from ...models.multiple_select_field_field_serializer_with_related_fields import (
    MultipleSelectFieldFieldSerializerWithRelatedFields,
)
from ...models.number_field_field_serializer_with_related_fields import NumberFieldFieldSerializerWithRelatedFields
from ...models.phone_number_field_field_serializer_with_related_fields import (
    PhoneNumberFieldFieldSerializerWithRelatedFields,
)
from ...models.rating_field_field_serializer_with_related_fields import RatingFieldFieldSerializerWithRelatedFields
from ...models.request_boolean_field_update_field import RequestBooleanFieldUpdateField
from ...models.request_created_on_field_update_field import RequestCreatedOnFieldUpdateField
from ...models.request_date_field_update_field import RequestDateFieldUpdateField
from ...models.request_email_field_update_field import RequestEmailFieldUpdateField
from ...models.request_file_field_update_field import RequestFileFieldUpdateField
from ...models.request_formula_field_update_field import RequestFormulaFieldUpdateField
from ...models.request_last_modified_field_update_field import RequestLastModifiedFieldUpdateField
from ...models.request_link_row_field_update_field import RequestLinkRowFieldUpdateField
from ...models.request_long_text_field_update_field import RequestLongTextFieldUpdateField
from ...models.request_lookup_field_update_field import RequestLookupFieldUpdateField
from ...models.request_multiple_collaborators_field_update_field import RequestMultipleCollaboratorsFieldUpdateField
from ...models.request_multiple_select_field_update_field import RequestMultipleSelectFieldUpdateField
from ...models.request_number_field_update_field import RequestNumberFieldUpdateField
from ...models.request_phone_number_field_update_field import RequestPhoneNumberFieldUpdateField
from ...models.request_rating_field_update_field import RequestRatingFieldUpdateField
from ...models.request_single_select_field_update_field import RequestSingleSelectFieldUpdateField
from ...models.request_text_field_update_field import RequestTextFieldUpdateField
from ...models.request_url_field_update_field import RequestURLFieldUpdateField
from ...models.single_select_field_field_serializer_with_related_fields import (
    SingleSelectFieldFieldSerializerWithRelatedFields,
)
from ...models.text_field_field_serializer_with_related_fields import TextFieldFieldSerializerWithRelatedFields
from ...models.update_database_table_field_response_400 import UpdateDatabaseTableFieldResponse400
from ...models.update_database_table_field_response_404 import UpdateDatabaseTableFieldResponse404
from ...models.url_field_field_serializer_with_related_fields import URLFieldFieldSerializerWithRelatedFields
from ...types import UNSET, Response, Unset


def _get_kwargs(
    field_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestBooleanFieldUpdateField",
        "RequestCreatedOnFieldUpdateField",
        "RequestDateFieldUpdateField",
        "RequestEmailFieldUpdateField",
        "RequestFileFieldUpdateField",
        "RequestFormulaFieldUpdateField",
        "RequestLastModifiedFieldUpdateField",
        "RequestLinkRowFieldUpdateField",
        "RequestLongTextFieldUpdateField",
        "RequestLookupFieldUpdateField",
        "RequestMultipleCollaboratorsFieldUpdateField",
        "RequestMultipleSelectFieldUpdateField",
        "RequestNumberFieldUpdateField",
        "RequestPhoneNumberFieldUpdateField",
        "RequestRatingFieldUpdateField",
        "RequestSingleSelectFieldUpdateField",
        "RequestTextFieldUpdateField",
        "RequestURLFieldUpdateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/database/fields/{field_id}/".format(client.base_url, field_id=field_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(client_session_id, Unset):
        headers["ClientSessionId"] = client_session_id

    if not isinstance(client_undo_redo_action_group_id, Unset):
        headers["ClientUndoRedoActionGroupId"] = client_undo_redo_action_group_id

    json_json_body: Dict[str, Any]

    if isinstance(json_body, RequestTextFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestLongTextFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestURLFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestEmailFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestNumberFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestRatingFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestBooleanFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestDateFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestLastModifiedFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestCreatedOnFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestLinkRowFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestFileFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestSingleSelectFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestMultipleSelectFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestPhoneNumberFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestFormulaFieldUpdateField):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, RequestLookupFieldUpdateField):
        json_json_body = json_body.to_dict()

    else:
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
) -> Optional[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
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
        response_400 = UpdateDatabaseTableFieldResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateDatabaseTableFieldResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestBooleanFieldUpdateField",
        "RequestCreatedOnFieldUpdateField",
        "RequestDateFieldUpdateField",
        "RequestEmailFieldUpdateField",
        "RequestFileFieldUpdateField",
        "RequestFormulaFieldUpdateField",
        "RequestLastModifiedFieldUpdateField",
        "RequestLinkRowFieldUpdateField",
        "RequestLongTextFieldUpdateField",
        "RequestLookupFieldUpdateField",
        "RequestMultipleCollaboratorsFieldUpdateField",
        "RequestMultipleSelectFieldUpdateField",
        "RequestNumberFieldUpdateField",
        "RequestPhoneNumberFieldUpdateField",
        "RequestRatingFieldUpdateField",
        "RequestSingleSelectFieldUpdateField",
        "RequestTextFieldUpdateField",
        "RequestURLFieldUpdateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
    ]
]:
    """Updates the existing field if the authorized user has access to the related database's workspace.
    The type can also be changed and depending on that type, different additional properties can
    optionally be set. If you change the field type it could happen that the data conversion fails, in
    that case the `ERROR_CANNOT_CHANGE_FIELD_TYPE` is returned, but this rarely happens. If a data value
    cannot be converted it is set to `null` so data might go lost.If updated the field causes other
    fields to change then the specificinstances of those fields will be included in the related fields
    response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['RequestBooleanFieldUpdateField', 'RequestCreatedOnFieldUpdateField',
            'RequestDateFieldUpdateField', 'RequestEmailFieldUpdateField',
            'RequestFileFieldUpdateField', 'RequestFormulaFieldUpdateField',
            'RequestLastModifiedFieldUpdateField', 'RequestLinkRowFieldUpdateField',
            'RequestLongTextFieldUpdateField', 'RequestLookupFieldUpdateField',
            'RequestMultipleCollaboratorsFieldUpdateField', 'RequestMultipleSelectFieldUpdateField',
            'RequestNumberFieldUpdateField', 'RequestPhoneNumberFieldUpdateField',
            'RequestRatingFieldUpdateField', 'RequestSingleSelectFieldUpdateField',
            'RequestTextFieldUpdateField', 'RequestURLFieldUpdateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields'], UpdateDatabaseTableFieldResponse400, UpdateDatabaseTableFieldResponse404]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
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
    field_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestBooleanFieldUpdateField",
        "RequestCreatedOnFieldUpdateField",
        "RequestDateFieldUpdateField",
        "RequestEmailFieldUpdateField",
        "RequestFileFieldUpdateField",
        "RequestFormulaFieldUpdateField",
        "RequestLastModifiedFieldUpdateField",
        "RequestLinkRowFieldUpdateField",
        "RequestLongTextFieldUpdateField",
        "RequestLookupFieldUpdateField",
        "RequestMultipleCollaboratorsFieldUpdateField",
        "RequestMultipleSelectFieldUpdateField",
        "RequestNumberFieldUpdateField",
        "RequestPhoneNumberFieldUpdateField",
        "RequestRatingFieldUpdateField",
        "RequestSingleSelectFieldUpdateField",
        "RequestTextFieldUpdateField",
        "RequestURLFieldUpdateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
    ]
]:
    """Updates the existing field if the authorized user has access to the related database's workspace.
    The type can also be changed and depending on that type, different additional properties can
    optionally be set. If you change the field type it could happen that the data conversion fails, in
    that case the `ERROR_CANNOT_CHANGE_FIELD_TYPE` is returned, but this rarely happens. If a data value
    cannot be converted it is set to `null` so data might go lost.If updated the field causes other
    fields to change then the specificinstances of those fields will be included in the related fields
    response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['RequestBooleanFieldUpdateField', 'RequestCreatedOnFieldUpdateField',
            'RequestDateFieldUpdateField', 'RequestEmailFieldUpdateField',
            'RequestFileFieldUpdateField', 'RequestFormulaFieldUpdateField',
            'RequestLastModifiedFieldUpdateField', 'RequestLinkRowFieldUpdateField',
            'RequestLongTextFieldUpdateField', 'RequestLookupFieldUpdateField',
            'RequestMultipleCollaboratorsFieldUpdateField', 'RequestMultipleSelectFieldUpdateField',
            'RequestNumberFieldUpdateField', 'RequestPhoneNumberFieldUpdateField',
            'RequestRatingFieldUpdateField', 'RequestSingleSelectFieldUpdateField',
            'RequestTextFieldUpdateField', 'RequestURLFieldUpdateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields'], UpdateDatabaseTableFieldResponse400, UpdateDatabaseTableFieldResponse404]
    """

    return sync_detailed(
        field_id=field_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    ).parsed


async def asyncio_detailed(
    field_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestBooleanFieldUpdateField",
        "RequestCreatedOnFieldUpdateField",
        "RequestDateFieldUpdateField",
        "RequestEmailFieldUpdateField",
        "RequestFileFieldUpdateField",
        "RequestFormulaFieldUpdateField",
        "RequestLastModifiedFieldUpdateField",
        "RequestLinkRowFieldUpdateField",
        "RequestLongTextFieldUpdateField",
        "RequestLookupFieldUpdateField",
        "RequestMultipleCollaboratorsFieldUpdateField",
        "RequestMultipleSelectFieldUpdateField",
        "RequestNumberFieldUpdateField",
        "RequestPhoneNumberFieldUpdateField",
        "RequestRatingFieldUpdateField",
        "RequestSingleSelectFieldUpdateField",
        "RequestTextFieldUpdateField",
        "RequestURLFieldUpdateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Response[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
    ]
]:
    """Updates the existing field if the authorized user has access to the related database's workspace.
    The type can also be changed and depending on that type, different additional properties can
    optionally be set. If you change the field type it could happen that the data conversion fails, in
    that case the `ERROR_CANNOT_CHANGE_FIELD_TYPE` is returned, but this rarely happens. If a data value
    cannot be converted it is set to `null` so data might go lost.If updated the field causes other
    fields to change then the specificinstances of those fields will be included in the related fields
    response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['RequestBooleanFieldUpdateField', 'RequestCreatedOnFieldUpdateField',
            'RequestDateFieldUpdateField', 'RequestEmailFieldUpdateField',
            'RequestFileFieldUpdateField', 'RequestFormulaFieldUpdateField',
            'RequestLastModifiedFieldUpdateField', 'RequestLinkRowFieldUpdateField',
            'RequestLongTextFieldUpdateField', 'RequestLookupFieldUpdateField',
            'RequestMultipleCollaboratorsFieldUpdateField', 'RequestMultipleSelectFieldUpdateField',
            'RequestNumberFieldUpdateField', 'RequestPhoneNumberFieldUpdateField',
            'RequestRatingFieldUpdateField', 'RequestSingleSelectFieldUpdateField',
            'RequestTextFieldUpdateField', 'RequestURLFieldUpdateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields'], UpdateDatabaseTableFieldResponse400, UpdateDatabaseTableFieldResponse404]]
    """

    kwargs = _get_kwargs(
        field_id=field_id,
        client=client,
        json_body=json_body,
        client_session_id=client_session_id,
        client_undo_redo_action_group_id=client_undo_redo_action_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    field_id: int,
    *,
    client: AuthenticatedClient,
    json_body: Union[
        "RequestBooleanFieldUpdateField",
        "RequestCreatedOnFieldUpdateField",
        "RequestDateFieldUpdateField",
        "RequestEmailFieldUpdateField",
        "RequestFileFieldUpdateField",
        "RequestFormulaFieldUpdateField",
        "RequestLastModifiedFieldUpdateField",
        "RequestLinkRowFieldUpdateField",
        "RequestLongTextFieldUpdateField",
        "RequestLookupFieldUpdateField",
        "RequestMultipleCollaboratorsFieldUpdateField",
        "RequestMultipleSelectFieldUpdateField",
        "RequestNumberFieldUpdateField",
        "RequestPhoneNumberFieldUpdateField",
        "RequestRatingFieldUpdateField",
        "RequestSingleSelectFieldUpdateField",
        "RequestTextFieldUpdateField",
        "RequestURLFieldUpdateField",
    ],
    client_session_id: Union[Unset, str] = UNSET,
    client_undo_redo_action_group_id: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
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
        UpdateDatabaseTableFieldResponse400,
        UpdateDatabaseTableFieldResponse404,
    ]
]:
    """Updates the existing field if the authorized user has access to the related database's workspace.
    The type can also be changed and depending on that type, different additional properties can
    optionally be set. If you change the field type it could happen that the data conversion fails, in
    that case the `ERROR_CANNOT_CHANGE_FIELD_TYPE` is returned, but this rarely happens. If a data value
    cannot be converted it is set to `null` so data might go lost.If updated the field causes other
    fields to change then the specificinstances of those fields will be included in the related fields
    response key.

    Args:
        field_id (int):
        client_session_id (Union[Unset, str]):
        client_undo_redo_action_group_id (Union[Unset, str]):
        json_body (Union['RequestBooleanFieldUpdateField', 'RequestCreatedOnFieldUpdateField',
            'RequestDateFieldUpdateField', 'RequestEmailFieldUpdateField',
            'RequestFileFieldUpdateField', 'RequestFormulaFieldUpdateField',
            'RequestLastModifiedFieldUpdateField', 'RequestLinkRowFieldUpdateField',
            'RequestLongTextFieldUpdateField', 'RequestLookupFieldUpdateField',
            'RequestMultipleCollaboratorsFieldUpdateField', 'RequestMultipleSelectFieldUpdateField',
            'RequestNumberFieldUpdateField', 'RequestPhoneNumberFieldUpdateField',
            'RequestRatingFieldUpdateField', 'RequestSingleSelectFieldUpdateField',
            'RequestTextFieldUpdateField', 'RequestURLFieldUpdateField']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Union['BooleanFieldFieldSerializerWithRelatedFields', 'CreatedOnFieldFieldSerializerWithRelatedFields', 'DateFieldFieldSerializerWithRelatedFields', 'EmailFieldFieldSerializerWithRelatedFields', 'FileFieldFieldSerializerWithRelatedFields', 'FormulaFieldFieldSerializerWithRelatedFields', 'LastModifiedFieldFieldSerializerWithRelatedFields', 'LinkRowFieldFieldSerializerWithRelatedFields', 'LongTextFieldFieldSerializerWithRelatedFields', 'LookupFieldFieldSerializerWithRelatedFields', 'MultipleCollaboratorsFieldFieldSerializerWithRelatedFields', 'MultipleSelectFieldFieldSerializerWithRelatedFields', 'NumberFieldFieldSerializerWithRelatedFields', 'PhoneNumberFieldFieldSerializerWithRelatedFields', 'RatingFieldFieldSerializerWithRelatedFields', 'SingleSelectFieldFieldSerializerWithRelatedFields', 'TextFieldFieldSerializerWithRelatedFields', 'URLFieldFieldSerializerWithRelatedFields'], UpdateDatabaseTableFieldResponse400, UpdateDatabaseTableFieldResponse404]
    """

    return (
        await asyncio_detailed(
            field_id=field_id,
            client=client,
            json_body=json_body,
            client_session_id=client_session_id,
            client_undo_redo_action_group_id=client_undo_redo_action_group_id,
        )
    ).parsed
