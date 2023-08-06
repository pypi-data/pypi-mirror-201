from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CalendarViewUpdate")


@attr.s(auto_attribs=True)
class CalendarViewUpdate:
    """
    Attributes:
        name (Union[Unset, str]):
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
        public_view_password (Union[Unset, str]): The password required to access the public view URL.
        date_field (Union[Unset, None, int]):
    """

    name: Union[Unset, str] = UNSET
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
    public_view_password: Union[Unset, str] = UNSET
    date_field: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters_disabled = self.filters_disabled
        public_view_password = self.public_view_password
        date_field = self.date_field

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
        if public_view_password is not UNSET:
            field_dict["public_view_password"] = public_view_password
        if date_field is not UNSET:
            field_dict["date_field"] = date_field

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters_disabled = d.pop("filters_disabled", UNSET)

        public_view_password = d.pop("public_view_password", UNSET)

        date_field = d.pop("date_field", UNSET)

        calendar_view_update = cls(
            name=name,
            filter_type=filter_type,
            filters_disabled=filters_disabled,
            public_view_password=public_view_password,
            date_field=date_field,
        )

        calendar_view_update.additional_properties = d
        return calendar_view_update

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
