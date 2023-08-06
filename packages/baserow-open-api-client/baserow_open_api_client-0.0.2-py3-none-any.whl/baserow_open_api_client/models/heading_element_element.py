from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HeadingElementElement")


@attr.s(auto_attribs=True)
class HeadingElementElement:
    """Basic element serializer mostly for returned values.

    Attributes:
        id (int):
        page_id (int):
        type (str): The type of the element.
        order (str): Lowest first.
        value (Union[Unset, str]): The value of the element. Must be an expression. Default: ''.
        level (Union[Unset, int]): The level of the heading from 1 to 6. Default: 1.
    """

    id: int
    page_id: int
    type: str
    order: str
    value: Union[Unset, str] = ""
    level: Union[Unset, int] = 1
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        page_id = self.page_id
        type = self.type
        order = self.order
        value = self.value
        level = self.level

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "page_id": page_id,
                "type": type,
                "order": order,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        page_id = d.pop("page_id")

        type = d.pop("type")

        order = d.pop("order")

        value = d.pop("value", UNSET)

        level = d.pop("level", UNSET)

        heading_element_element = cls(
            id=id,
            page_id=page_id,
            type=type,
            order=order,
            value=value,
            level=level,
        )

        heading_element_element.additional_properties = d
        return heading_element_element

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
