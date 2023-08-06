from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SamlAuthProviderModelAuthProvider")


@attr.s(auto_attribs=True)
class SamlAuthProviderModelAuthProvider:
    """
    Attributes:
        id (int):
        type (str): The type of the related field.
        domain (str): The email domain registered with this provider.
        metadata (str): The SAML metadata XML provided by the IdP.
        is_verified (bool): Whether or not a user sign in correctly with this SAML provider.
        enabled (Union[Unset, bool]): Whether the provider is enabled or not.
    """

    id: int
    type: str
    domain: str
    metadata: str
    is_verified: bool
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        domain = self.domain
        metadata = self.metadata
        is_verified = self.is_verified
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "domain": domain,
                "metadata": metadata,
                "is_verified": is_verified,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        domain = d.pop("domain")

        metadata = d.pop("metadata")

        is_verified = d.pop("is_verified")

        enabled = d.pop("enabled", UNSET)

        saml_auth_provider_model_auth_provider = cls(
            id=id,
            type=type,
            domain=domain,
            metadata=metadata,
            is_verified=is_verified,
            enabled=enabled,
        )

        saml_auth_provider_model_auth_provider.additional_properties = d
        return saml_auth_provider_model_auth_provider

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
