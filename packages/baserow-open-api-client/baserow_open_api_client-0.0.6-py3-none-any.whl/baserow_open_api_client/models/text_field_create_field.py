from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="TextFieldCreateField")


@attr.s(auto_attribs=True)
class TextFieldCreateField:
    """
    Attributes:
        name (str):
        type (Type77BEnum):
        text_default (Union[Unset, str]): If set, this value is going to be added every time a new row created.
    """

    name: str
    type: Type77BEnum
    text_default: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        text_default = self.text_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if text_default is not UNSET:
            field_dict["text_default"] = text_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = Type77BEnum(d.pop("type"))

        text_default = d.pop("text_default", UNSET)

        text_field_create_field = cls(
            name=name,
            type=type,
            text_default=text_default,
        )

        text_field_create_field.additional_properties = d
        return text_field_create_field

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
