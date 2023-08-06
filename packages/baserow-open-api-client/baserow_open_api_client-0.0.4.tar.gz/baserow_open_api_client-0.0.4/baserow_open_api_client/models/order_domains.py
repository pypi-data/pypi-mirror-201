from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="OrderDomains")


@attr.s(auto_attribs=True)
class OrderDomains:
    """
    Attributes:
        domain_ids (List[int]): The ids of the domains in the order they are supposed to be set in
    """

    domain_ids: List[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain_ids = self.domain_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain_ids": domain_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        domain_ids = cast(List[int], d.pop("domain_ids"))

        order_domains = cls(
            domain_ids=domain_ids,
        )

        order_domains.additional_properties = d
        return order_domains

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
