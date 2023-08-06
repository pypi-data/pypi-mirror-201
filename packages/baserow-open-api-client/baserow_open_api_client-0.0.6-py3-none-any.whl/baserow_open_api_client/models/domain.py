from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="Domain")


@attr.s(auto_attribs=True)
class Domain:
    """
    Attributes:
        id (int):
        domain_name (str):
        order (int): Lowest first.
        builder_id (int):
    """

    id: int
    domain_name: str
    order: int
    builder_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        domain_name = self.domain_name
        order = self.order
        builder_id = self.builder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "domain_name": domain_name,
                "order": order,
                "builder_id": builder_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        domain_name = d.pop("domain_name")

        order = d.pop("order")

        builder_id = d.pop("builder_id")

        domain = cls(
            id=id,
            domain_name=domain_name,
            order=order,
            builder_id=builder_id,
        )

        domain.additional_properties = d
        return domain

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
