from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkRowFieldField")


@attr.s(auto_attribs=True)
class LinkRowFieldField:
    """
    Attributes:
        id (int):
        table_id (int):
        name (str):
        order (int): Lowest first.
        type (str): The type of the related field.
        read_only (bool): Indicates whether the field is a read only field. If true, it's not possible to update the
            cell value.
        link_row_related_field (int): (Deprecated) The id of the related field.
        primary (Union[Unset, bool]): Indicates if the field is a primary field. If `true` the field cannot be deleted
            and the value should represent the whole row.
        link_row_table_id (Union[Unset, None, int]): The id of the linked table.
        link_row_related_field_id (Optional[int]): The id of the related field.
        link_row_table (Union[Unset, None, int]): (Deprecated) The id of the linked table.
    """

    id: int
    table_id: int
    name: str
    order: int
    type: str
    read_only: bool
    link_row_related_field: int
    link_row_related_field_id: Optional[int]
    primary: Union[Unset, bool] = UNSET
    link_row_table_id: Union[Unset, None, int] = UNSET
    link_row_table: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        name = self.name
        order = self.order
        type = self.type
        read_only = self.read_only
        link_row_related_field = self.link_row_related_field
        primary = self.primary
        link_row_table_id = self.link_row_table_id
        link_row_related_field_id = self.link_row_related_field_id
        link_row_table = self.link_row_table

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "name": name,
                "order": order,
                "type": type,
                "read_only": read_only,
                "link_row_related_field": link_row_related_field,
                "link_row_related_field_id": link_row_related_field_id,
            }
        )
        if primary is not UNSET:
            field_dict["primary"] = primary
        if link_row_table_id is not UNSET:
            field_dict["link_row_table_id"] = link_row_table_id
        if link_row_table is not UNSET:
            field_dict["link_row_table"] = link_row_table

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        read_only = d.pop("read_only")

        link_row_related_field = d.pop("link_row_related_field")

        primary = d.pop("primary", UNSET)

        link_row_table_id = d.pop("link_row_table_id", UNSET)

        link_row_related_field_id = d.pop("link_row_related_field_id")

        link_row_table = d.pop("link_row_table", UNSET)

        link_row_field_field = cls(
            id=id,
            table_id=table_id,
            name=name,
            order=order,
            type=type,
            read_only=read_only,
            link_row_related_field=link_row_related_field,
            primary=primary,
            link_row_table_id=link_row_table_id,
            link_row_related_field_id=link_row_related_field_id,
            link_row_table=link_row_table,
        )

        link_row_field_field.additional_properties = d
        return link_row_field_field

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
