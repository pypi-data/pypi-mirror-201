from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Table")


@attr.s(auto_attribs=True)
class Table:
    """
    Attributes:
        id (int):
        name (str):
        order (int): Lowest first.
        database_id (int):
    """

    id: int
    name: str
    order: int
    database_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        order = self.order
        database_id = self.database_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "order": order,
                "database_id": database_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        order = d.pop("order")

        database_id = d.pop("database_id")

        table = cls(
            id=id,
            name=name,
            order=order,
            database_id=database_id,
        )

        table.additional_properties = d
        return table

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
