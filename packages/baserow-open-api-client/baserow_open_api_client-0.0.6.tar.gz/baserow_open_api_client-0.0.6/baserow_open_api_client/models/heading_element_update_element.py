from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HeadingElementUpdateElement")


@attr.s(auto_attribs=True)
class HeadingElementUpdateElement:
    """
    Attributes:
        value (Union[Unset, str]): The value of the element. Must be an expression. Default: ''.
        level (Union[Unset, int]): The level of the heading from 1 to 6. Default: 1.
    """

    value: Union[Unset, str] = ""
    level: Union[Unset, int] = 1
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        level = self.level

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        level = d.pop("level", UNSET)

        heading_element_update_element = cls(
            value=value,
            level=level,
        )

        heading_element_update_element.additional_properties = d
        return heading_element_update_element

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
