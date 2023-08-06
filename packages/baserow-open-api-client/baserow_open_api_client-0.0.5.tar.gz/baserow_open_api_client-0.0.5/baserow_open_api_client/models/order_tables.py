from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="OrderTables")


@attr.s(auto_attribs=True)
class OrderTables:
    """
    Attributes:
        table_ids (List[int]): Table ids in the desired order.
    """

    table_ids: List[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        table_ids = self.table_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "table_ids": table_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table_ids = cast(List[int], d.pop("table_ids"))

        order_tables = cls(
            table_ids=table_ids,
        )

        order_tables.additional_properties = d
        return order_tables

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
