import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.collaborator import Collaborator
    from ..models.file_field_response import FileFieldResponse
    from ..models.link_row_value import LinkRowValue
    from ..models.select_option import SelectOption


T = TypeVar("T", bound="ExampleRowResponse")


@attr.s(auto_attribs=True)
class ExampleRowResponse:
    """
    Attributes:
        id (int): The unique identifier of the row in the table.
        order (Union[Unset, str]): Indicates the position of the row, lowest first and highest last.
        field_1 (Union[Unset, None, str]): This field represents the `text` field. The number in field_1 is in a normal
            request or response the id of the field.
        field_2 (Union[Unset, None, str]): This field represents the `long_text` field. The number in field_2 is in a
            normal request or response the id of the field.
        field_3 (Union[Unset, None, str]): This field represents the `url` field. The number in field_3 is in a normal
            request or response the id of the field.
        field_4 (Union[Unset, None, str]): This field represents the `email` field. The number in field_4 is in a normal
            request or response the id of the field.
        field_5 (Union[Unset, None, str]): This field represents the `number` field. The number in field_5 is in a
            normal request or response the id of the field.
        field_6 (Union[Unset, int]): This field represents the `rating` field. The number in field_6 is in a normal
            request or response the id of the field.
        field_7 (Union[Unset, bool]): This field represents the `boolean` field. The number in field_7 is in a normal
            request or response the id of the field.
        field_8 (Union[Unset, None, datetime.date]): This field represents the `date` field. The number in field_8 is in
            a normal request or response the id of the field.
        field_9 (Union[Unset, datetime.datetime]): This field represents the `last_modified` field. The number in
            field_9 is in a normal request or response the id of the field.
        field_10 (Union[Unset, datetime.datetime]): This field represents the `created_on` field. The number in field_10
            is in a normal request or response the id of the field.
        field_11 (Union[Unset, List['LinkRowValue']]): This field represents the `link_row` field. The number in
            field_11 is in a normal request or response the id of the field.This field accepts an `array` containing the ids
            or the names of the related rows. In case of names, if the name is not found, this name is ignored. A name is
            the value of the primary key of the related row.The response contains a list of objects containing the `id` and
            the primary field's `value` as a string for display purposes.
        field_12 (Union[Unset, List['FileFieldResponse']]): This field represents the `file` field. The number in
            field_12 is in a normal request or response the id of the field.This field accepts an `array` containing objects
            with the name of the file. The response contains an `array` of more detailed objects related to the files.
        field_13 (Union[Unset, None, SelectOption]):
        field_14 (Union[Unset, None, List['SelectOption']]): This field represents the `multiple_select` field. The
            number in field_14 is in a normal request or response the id of the field.This field accepts a list of `integer`
            each of which representing the chosen select option id related to the field. Available ids can be foundwhen
            getting or listing the field. The response represents chosen field, but also the value and color is exposed.
        field_15 (Union[Unset, None, str]): This field represents the `phone_number` field. The number in field_15 is in
            a normal request or response the id of the field.
        field_16 (Union[Unset, None, str]): This field represents the `formula` field. The number in field_16 is in a
            normal request or response the id of the field.
        field_17 (Union[Unset, None, str]): This field represents the `lookup` field. The number in field_17 is in a
            normal request or response the id of the field.
        field_18 (Union[Unset, List['Collaborator']]): This field represents the `multiple_collaborators` field. The
            number in field_18 is in a normal request or response the id of the field.This field accepts a list of objects
            representing the chosen collaborators through the object's `id` property. The id is Baserow user id. The
            response objects also contains the collaborator name directly along with its id.
    """

    id: int
    order: Union[Unset, str] = UNSET
    field_1: Union[Unset, None, str] = UNSET
    field_2: Union[Unset, None, str] = UNSET
    field_3: Union[Unset, None, str] = UNSET
    field_4: Union[Unset, None, str] = UNSET
    field_5: Union[Unset, None, str] = UNSET
    field_6: Union[Unset, int] = 0
    field_7: Union[Unset, bool] = False
    field_8: Union[Unset, None, datetime.date] = UNSET
    field_9: Union[Unset, datetime.datetime] = UNSET
    field_10: Union[Unset, datetime.datetime] = UNSET
    field_11: Union[Unset, List["LinkRowValue"]] = UNSET
    field_12: Union[Unset, List["FileFieldResponse"]] = UNSET
    field_13: Union[Unset, None, "SelectOption"] = UNSET
    field_14: Union[Unset, None, List["SelectOption"]] = UNSET
    field_15: Union[Unset, None, str] = UNSET
    field_16: Union[Unset, None, str] = UNSET
    field_17: Union[Unset, None, str] = UNSET
    field_18: Union[Unset, List["Collaborator"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        order = self.order
        field_1 = self.field_1
        field_2 = self.field_2
        field_3 = self.field_3
        field_4 = self.field_4
        field_5 = self.field_5
        field_6 = self.field_6
        field_7 = self.field_7
        field_8: Union[Unset, None, str] = UNSET
        if not isinstance(self.field_8, Unset):
            field_8 = self.field_8.isoformat() if self.field_8 else None

        field_9: Union[Unset, str] = UNSET
        if not isinstance(self.field_9, Unset):
            field_9 = self.field_9.isoformat()

        field_10: Union[Unset, str] = UNSET
        if not isinstance(self.field_10, Unset):
            field_10 = self.field_10.isoformat()

        field_11: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_11, Unset):
            field_11 = []
            for field_11_item_data in self.field_11:
                field_11_item = field_11_item_data.to_dict()

                field_11.append(field_11_item)

        field_12: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_12, Unset):
            field_12 = []
            for field_12_item_data in self.field_12:
                field_12_item = field_12_item_data.to_dict()

                field_12.append(field_12_item)

        field_13: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.field_13, Unset):
            field_13 = self.field_13.to_dict() if self.field_13 else None

        field_14: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_14, Unset):
            if self.field_14 is None:
                field_14 = None
            else:
                field_14 = []
                for field_14_item_data in self.field_14:
                    field_14_item = field_14_item_data.to_dict()

                    field_14.append(field_14_item)

        field_15 = self.field_15
        field_16 = self.field_16
        field_17 = self.field_17
        field_18: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_18, Unset):
            field_18 = []
            for field_18_item_data in self.field_18:
                field_18_item = field_18_item_data.to_dict()

                field_18.append(field_18_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if order is not UNSET:
            field_dict["order"] = order
        if field_1 is not UNSET:
            field_dict["field_1"] = field_1
        if field_2 is not UNSET:
            field_dict["field_2"] = field_2
        if field_3 is not UNSET:
            field_dict["field_3"] = field_3
        if field_4 is not UNSET:
            field_dict["field_4"] = field_4
        if field_5 is not UNSET:
            field_dict["field_5"] = field_5
        if field_6 is not UNSET:
            field_dict["field_6"] = field_6
        if field_7 is not UNSET:
            field_dict["field_7"] = field_7
        if field_8 is not UNSET:
            field_dict["field_8"] = field_8
        if field_9 is not UNSET:
            field_dict["field_9"] = field_9
        if field_10 is not UNSET:
            field_dict["field_10"] = field_10
        if field_11 is not UNSET:
            field_dict["field_11"] = field_11
        if field_12 is not UNSET:
            field_dict["field_12"] = field_12
        if field_13 is not UNSET:
            field_dict["field_13"] = field_13
        if field_14 is not UNSET:
            field_dict["field_14"] = field_14
        if field_15 is not UNSET:
            field_dict["field_15"] = field_15
        if field_16 is not UNSET:
            field_dict["field_16"] = field_16
        if field_17 is not UNSET:
            field_dict["field_17"] = field_17
        if field_18 is not UNSET:
            field_dict["field_18"] = field_18

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.collaborator import Collaborator
        from ..models.file_field_response import FileFieldResponse
        from ..models.link_row_value import LinkRowValue
        from ..models.select_option import SelectOption

        d = src_dict.copy()
        id = d.pop("id")

        order = d.pop("order", UNSET)

        field_1 = d.pop("field_1", UNSET)

        field_2 = d.pop("field_2", UNSET)

        field_3 = d.pop("field_3", UNSET)

        field_4 = d.pop("field_4", UNSET)

        field_5 = d.pop("field_5", UNSET)

        field_6 = d.pop("field_6", UNSET)

        field_7 = d.pop("field_7", UNSET)

        _field_8 = d.pop("field_8", UNSET)
        field_8: Union[Unset, None, datetime.date]
        if _field_8 is None:
            field_8 = None
        elif isinstance(_field_8, Unset):
            field_8 = UNSET
        else:
            field_8 = isoparse(_field_8).date()

        _field_9 = d.pop("field_9", UNSET)
        field_9: Union[Unset, datetime.datetime]
        if isinstance(_field_9, Unset):
            field_9 = UNSET
        else:
            field_9 = isoparse(_field_9)

        _field_10 = d.pop("field_10", UNSET)
        field_10: Union[Unset, datetime.datetime]
        if isinstance(_field_10, Unset):
            field_10 = UNSET
        else:
            field_10 = isoparse(_field_10)

        field_11 = []
        _field_11 = d.pop("field_11", UNSET)
        for field_11_item_data in _field_11 or []:
            field_11_item = LinkRowValue.from_dict(field_11_item_data)

            field_11.append(field_11_item)

        field_12 = []
        _field_12 = d.pop("field_12", UNSET)
        for field_12_item_data in _field_12 or []:
            field_12_item = FileFieldResponse.from_dict(field_12_item_data)

            field_12.append(field_12_item)

        _field_13 = d.pop("field_13", UNSET)
        field_13: Union[Unset, None, SelectOption]
        if _field_13 is None:
            field_13 = None
        elif isinstance(_field_13, Unset):
            field_13 = UNSET
        else:
            field_13 = SelectOption.from_dict(_field_13)

        field_14 = []
        _field_14 = d.pop("field_14", UNSET)
        for field_14_item_data in _field_14 or []:
            field_14_item = SelectOption.from_dict(field_14_item_data)

            field_14.append(field_14_item)

        field_15 = d.pop("field_15", UNSET)

        field_16 = d.pop("field_16", UNSET)

        field_17 = d.pop("field_17", UNSET)

        field_18 = []
        _field_18 = d.pop("field_18", UNSET)
        for field_18_item_data in _field_18 or []:
            field_18_item = Collaborator.from_dict(field_18_item_data)

            field_18.append(field_18_item)

        example_row_response = cls(
            id=id,
            order=order,
            field_1=field_1,
            field_2=field_2,
            field_3=field_3,
            field_4=field_4,
            field_5=field_5,
            field_6=field_6,
            field_7=field_7,
            field_8=field_8,
            field_9=field_9,
            field_10=field_10,
            field_11=field_11,
            field_12=field_12,
            field_13=field_13,
            field_14=field_14,
            field_15=field_15,
            field_16=field_16,
            field_17=field_17,
            field_18=field_18,
        )

        example_row_response.additional_properties = d
        return example_row_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
