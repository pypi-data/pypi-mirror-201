import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.collaborator import Collaborator
    from ..models.file_field_request import FileFieldRequest


T = TypeVar("T", bound="PatchedExampleUpdateRowRequestSerializerWithUserFieldNames")


@attr.s(auto_attribs=True)
class PatchedExampleUpdateRowRequestSerializerWithUserFieldNames:
    """
    Attributes:
        field_1 (Union[Unset, None, str]): This field represents the `text` field. The number in field_1 is in a normal
            request or response the id of the field. If the GET parameter `user_field_names` is provided then the key will
            instead be the actual name of the field.
        field_2 (Union[Unset, None, str]): This field represents the `long_text` field. The number in field_2 is in a
            normal request or response the id of the field. If the GET parameter `user_field_names` is provided then the key
            will instead be the actual name of the field.
        field_3 (Union[Unset, None, str]): This field represents the `url` field. The number in field_3 is in a normal
            request or response the id of the field. If the GET parameter `user_field_names` is provided then the key will
            instead be the actual name of the field.
        field_4 (Union[Unset, None, str]): This field represents the `email` field. The number in field_4 is in a normal
            request or response the id of the field. If the GET parameter `user_field_names` is provided then the key will
            instead be the actual name of the field.
        field_5 (Union[Unset, None, str]): This field represents the `number` field. The number in field_5 is in a
            normal request or response the id of the field. If the GET parameter `user_field_names` is provided then the key
            will instead be the actual name of the field.
        field_6 (Union[Unset, int]): This field represents the `rating` field. The number in field_6 is in a normal
            request or response the id of the field. If the GET parameter `user_field_names` is provided then the key will
            instead be the actual name of the field.
        field_7 (Union[Unset, bool]): This field represents the `boolean` field. The number in field_7 is in a normal
            request or response the id of the field. If the GET parameter `user_field_names` is provided then the key will
            instead be the actual name of the field.
        field_8 (Union[Unset, None, datetime.date]): This field represents the `date` field. The number in field_8 is in
            a normal request or response the id of the field. If the GET parameter `user_field_names` is provided then the
            key will instead be the actual name of the field.
        field_11 (Union[Unset, List[Optional[int]]]): This field represents the `link_row` field. The number in field_11
            is in a normal request or response the id of the field. If the GET parameter `user_field_names` is provided then
            the key will instead be the actual name of the field.This field accepts an `array` containing the ids or the
            names of the related rows. In case of names, if the name is not found, this name is ignored. A name is the value
            of the primary key of the related row.The response contains a list of objects containing the `id` and the
            primary field's `value` as a string for display purposes.
        field_12 (Union[Unset, None, List['FileFieldRequest']]): This field represents the `file` field. The number in
            field_12 is in a normal request or response the id of the field. If the GET parameter `user_field_names` is
            provided then the key will instead be the actual name of the field.This field accepts an `array` containing
            objects with the name of the file. The response contains an `array` of more detailed objects related to the
            files.
        field_13 (Union[Unset, None, int]): This field represents the `single_select` field. The number in field_13 is
            in a normal request or response the id of the field. If the GET parameter `user_field_names` is provided then
            the key will instead be the actual name of the field.This field accepts an `integer` representing the chosen
            select option id related to the field. Available ids can be found when getting or listing the field. The
            response represents chosen field, but also the value and color is exposed.
        field_14 (Union[Unset, List[Optional[int]]]): This field represents the `multiple_select` field. The number in
            field_14 is in a normal request or response the id of the field. If the GET parameter `user_field_names` is
            provided then the key will instead be the actual name of the field.This field accepts a list of `integer` each
            of which representing the chosen select option id related to the field. Available ids can be foundwhen getting
            or listing the field. The response represents chosen field, but also the value and color is exposed.
        field_15 (Union[Unset, None, str]): This field represents the `phone_number` field. The number in field_15 is in
            a normal request or response the id of the field. If the GET parameter `user_field_names` is provided then the
            key will instead be the actual name of the field.
        field_18 (Union[Unset, List['Collaborator']]): This field represents the `multiple_collaborators` field. The
            number in field_18 is in a normal request or response the id of the field. If the GET parameter
            `user_field_names` is provided then the key will instead be the actual name of the field.This field accepts a
            list of objects representing the chosen collaborators through the object's `id` property. The id is Baserow user
            id. The response objects also contains the collaborator name directly along with its id.
    """

    field_1: Union[Unset, None, str] = UNSET
    field_2: Union[Unset, None, str] = UNSET
    field_3: Union[Unset, None, str] = UNSET
    field_4: Union[Unset, None, str] = UNSET
    field_5: Union[Unset, None, str] = UNSET
    field_6: Union[Unset, int] = 0
    field_7: Union[Unset, bool] = False
    field_8: Union[Unset, None, datetime.date] = UNSET
    field_11: Union[Unset, List[Optional[int]]] = UNSET
    field_12: Union[Unset, None, List["FileFieldRequest"]] = UNSET
    field_13: Union[Unset, None, int] = UNSET
    field_14: Union[Unset, List[Optional[int]]] = UNSET
    field_15: Union[Unset, None, str] = UNSET
    field_18: Union[Unset, List["Collaborator"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        field_11: Union[Unset, List[Optional[int]]] = UNSET
        if not isinstance(self.field_11, Unset):
            field_11 = self.field_11

        field_12: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_12, Unset):
            if self.field_12 is None:
                field_12 = None
            else:
                field_12 = []
                for field_12_item_data in self.field_12:
                    field_12_item = field_12_item_data.to_dict()

                    field_12.append(field_12_item)

        field_13 = self.field_13
        field_14: Union[Unset, List[Optional[int]]] = UNSET
        if not isinstance(self.field_14, Unset):
            field_14 = self.field_14

        field_15 = self.field_15
        field_18: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.field_18, Unset):
            field_18 = []
            for field_18_item_data in self.field_18:
                field_18_item = field_18_item_data.to_dict()

                field_18.append(field_18_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if field_18 is not UNSET:
            field_dict["field_18"] = field_18

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.collaborator import Collaborator
        from ..models.file_field_request import FileFieldRequest

        d = src_dict.copy()
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

        field_11 = cast(List[Optional[int]], d.pop("field_11", UNSET))

        field_12 = []
        _field_12 = d.pop("field_12", UNSET)
        for field_12_item_data in _field_12 or []:
            field_12_item = FileFieldRequest.from_dict(field_12_item_data)

            field_12.append(field_12_item)

        field_13 = d.pop("field_13", UNSET)

        field_14 = cast(List[Optional[int]], d.pop("field_14", UNSET))

        field_15 = d.pop("field_15", UNSET)

        field_18 = []
        _field_18 = d.pop("field_18", UNSET)
        for field_18_item_data in _field_18 or []:
            field_18_item = Collaborator.from_dict(field_18_item_data)

            field_18.append(field_18_item)

        patched_example_update_row_request_serializer_with_user_field_names = cls(
            field_1=field_1,
            field_2=field_2,
            field_3=field_3,
            field_4=field_4,
            field_5=field_5,
            field_6=field_6,
            field_7=field_7,
            field_8=field_8,
            field_11=field_11,
            field_12=field_12,
            field_13=field_13,
            field_14=field_14,
            field_15=field_15,
            field_18=field_18,
        )

        patched_example_update_row_request_serializer_with_user_field_names.additional_properties = d
        return patched_example_update_row_request_serializer_with_user_field_names

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
