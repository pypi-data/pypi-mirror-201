from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.type_77b_enum import Type77BEnum

T = TypeVar("T", bound="BooleanFieldCreateField")


@attr.s(auto_attribs=True)
class BooleanFieldCreateField:
    """
    Attributes:
        name (str):
        type (Type77BEnum):
    """

    name: str
    type: Type77BEnum
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = Type77BEnum(d.pop("type"))

        boolean_field_create_field = cls(
            name=name,
            type=type,
        )

        boolean_field_create_field.additional_properties = d
        return boolean_field_create_field

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
