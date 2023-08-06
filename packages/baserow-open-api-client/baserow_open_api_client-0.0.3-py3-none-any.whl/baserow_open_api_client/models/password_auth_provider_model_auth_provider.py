from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PasswordAuthProviderModelAuthProvider")


@attr.s(auto_attribs=True)
class PasswordAuthProviderModelAuthProvider:
    """
    Attributes:
        id (int):
        type (str): The type of the related field.
        domain (Union[Unset, str]): The email domain (if any) registered with this password provider.
        enabled (Union[Unset, bool]): Whether the provider is enabled or not.
    """

    id: int
    type: str
    domain: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        domain = self.domain
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        domain = d.pop("domain", UNSET)

        enabled = d.pop("enabled", UNSET)

        password_auth_provider_model_auth_provider = cls(
            id=id,
            type=type,
            domain=domain,
            enabled=enabled,
        )

        password_auth_provider_model_auth_provider.additional_properties = d
        return password_auth_provider_model_auth_provider

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
