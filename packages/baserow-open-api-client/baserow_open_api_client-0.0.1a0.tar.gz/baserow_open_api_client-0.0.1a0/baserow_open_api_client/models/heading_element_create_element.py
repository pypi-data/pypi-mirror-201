from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_20d_enum import Type20DEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="HeadingElementCreateElement")


@attr.s(auto_attribs=True)
class HeadingElementCreateElement:
    """This serializer allow to set the type of an element and the element id before which
    we want to insert the new element.

        Attributes:
            type (Type20DEnum):
            before_id (Union[Unset, int]): If provided, creates the element before the element with the given id.
            value (Union[Unset, str]): The value of the element. Must be an expression. Default: ''.
            level (Union[Unset, int]): The level of the heading from 1 to 6. Default: 1.
    """

    type: Type20DEnum
    before_id: Union[Unset, int] = UNSET
    value: Union[Unset, str] = ""
    level: Union[Unset, int] = 1
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        before_id = self.before_id
        value = self.value
        level = self.level

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if before_id is not UNSET:
            field_dict["before_id"] = before_id
        if value is not UNSET:
            field_dict["value"] = value
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = Type20DEnum(d.pop("type"))

        before_id = d.pop("before_id", UNSET)

        value = d.pop("value", UNSET)

        level = d.pop("level", UNSET)

        heading_element_create_element = cls(
            type=type,
            before_id=before_id,
            value=value,
            level=level,
        )

        heading_element_create_element.additional_properties = d
        return heading_element_create_element

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
