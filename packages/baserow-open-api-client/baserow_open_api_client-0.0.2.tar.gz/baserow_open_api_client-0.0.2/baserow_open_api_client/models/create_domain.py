from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="CreateDomain")


@attr.s(auto_attribs=True)
class CreateDomain:
    """
    Attributes:
        domain_name (str):
    """

    domain_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain_name = self.domain_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "domain_name": domain_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        domain_name = d.pop("domain_name")

        create_domain = cls(
            domain_name=domain_name,
        )

        create_domain.additional_properties = d
        return create_domain

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
