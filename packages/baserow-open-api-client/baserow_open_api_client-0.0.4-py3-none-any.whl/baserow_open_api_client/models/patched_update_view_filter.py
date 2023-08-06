from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_9_cb_enum import Type9CbEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUpdateViewFilter")


@attr.s(auto_attribs=True)
class PatchedUpdateViewFilter:
    """
    Attributes:
        field (Union[Unset, int]): The field of which the value must be compared to the filter value.
        type (Union[Unset, Type9CbEnum]):
        value (Union[Unset, str]): The filter value that must be compared to the field's value.
    """

    field: Union[Unset, int] = UNSET
    type: Union[Unset, Type9CbEnum] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field = self.field
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, Type9CbEnum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = Type9CbEnum(_type)

        value = d.pop("value", UNSET)

        patched_update_view_filter = cls(
            field=field,
            type=type,
            value=value,
        )

        patched_update_view_filter.additional_properties = d
        return patched_update_view_filter

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
