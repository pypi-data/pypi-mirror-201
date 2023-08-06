from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.style_enum import StyleEnum
from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RatingFieldCreateField")


@attr.s(auto_attribs=True)
class RatingFieldCreateField:
    """
    Attributes:
        name (str):
        type (Type77BEnum):
        max_value (Union[Unset, int]): Maximum value the rating can take.
        color (Union[Unset, str]): Color of the symbols.
        style (Union[Unset, StyleEnum]):
    """

    name: str
    type: Type77BEnum
    max_value: Union[Unset, int] = UNSET
    color: Union[Unset, str] = UNSET
    style: Union[Unset, StyleEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        max_value = self.max_value
        color = self.color
        style: Union[Unset, str] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if max_value is not UNSET:
            field_dict["max_value"] = max_value
        if color is not UNSET:
            field_dict["color"] = color
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = Type77BEnum(d.pop("type"))

        max_value = d.pop("max_value", UNSET)

        color = d.pop("color", UNSET)

        _style = d.pop("style", UNSET)
        style: Union[Unset, StyleEnum]
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = StyleEnum(_style)

        rating_field_create_field = cls(
            name=name,
            type=type,
            max_value=max_value,
            color=color,
            style=style,
        )

        rating_field_create_field.additional_properties = d
        return rating_field_create_field

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
