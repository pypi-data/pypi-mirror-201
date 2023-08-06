from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_9_cb_enum import Type9CbEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateViewFilter")


@attr.s(auto_attribs=True)
class CreateViewFilter:
    """
    Attributes:
        field (int): The field of which the value must be compared to the filter value.
        type (Type9CbEnum):
        value (Union[Unset, str]): The filter value that must be compared to the field's value. Default: ''.
    """

    field: int
    type: Type9CbEnum
    value: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field = self.field
        type = self.type.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "type": type,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field")

        type = Type9CbEnum(d.pop("type"))

        value = d.pop("value", UNSET)

        create_view_filter = cls(
            field=field,
            type=type,
            value=value,
        )

        create_view_filter.additional_properties = d
        return create_view_filter

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
