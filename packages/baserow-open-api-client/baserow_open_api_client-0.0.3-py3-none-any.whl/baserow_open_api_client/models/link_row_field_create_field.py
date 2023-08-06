from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkRowFieldCreateField")


@attr.s(auto_attribs=True)
class LinkRowFieldCreateField:
    """
    Attributes:
        name (str):
        type (Type77BEnum):
        link_row_related_field (int): (Deprecated) The id of the related field.
        link_row_table_id (Union[Unset, None, int]): The id of the linked table.
        link_row_related_field_id (Optional[int]): The id of the related field.
        link_row_table (Union[Unset, None, int]): (Deprecated) The id of the linked table.
    """

    name: str
    type: Type77BEnum
    link_row_related_field: int
    link_row_related_field_id: Optional[int]
    link_row_table_id: Union[Unset, None, int] = UNSET
    link_row_table: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        link_row_related_field = self.link_row_related_field
        link_row_table_id = self.link_row_table_id
        link_row_related_field_id = self.link_row_related_field_id
        link_row_table = self.link_row_table

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
                "link_row_related_field": link_row_related_field,
                "link_row_related_field_id": link_row_related_field_id,
            }
        )
        if link_row_table_id is not UNSET:
            field_dict["link_row_table_id"] = link_row_table_id
        if link_row_table is not UNSET:
            field_dict["link_row_table"] = link_row_table

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = Type77BEnum(d.pop("type"))

        link_row_related_field = d.pop("link_row_related_field")

        link_row_table_id = d.pop("link_row_table_id", UNSET)

        link_row_related_field_id = d.pop("link_row_related_field_id")

        link_row_table = d.pop("link_row_table", UNSET)

        link_row_field_create_field = cls(
            name=name,
            type=type,
            link_row_related_field=link_row_related_field,
            link_row_table_id=link_row_table_id,
            link_row_related_field_id=link_row_related_field_id,
            link_row_table=link_row_table,
        )

        link_row_field_create_field.additional_properties = d
        return link_row_field_create_field

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
