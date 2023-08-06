from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GitLabAuthProviderModelAuthProvider")


@attr.s(auto_attribs=True)
class GitLabAuthProviderModelAuthProvider:
    """
    Attributes:
        id (int):
        type (str): The type of the related field.
        name (str):
        base_url (str): Base URL of the authorization server
        client_id (str): App ID, or consumer key
        secret (str): API secret, client secret, or consumer secret
        domain (Union[Unset, None, str]):
        enabled (Union[Unset, bool]):
    """

    id: int
    type: str
    name: str
    base_url: str
    client_id: str
    secret: str
    domain: Union[Unset, None, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        name = self.name
        base_url = self.base_url
        client_id = self.client_id
        secret = self.secret
        domain = self.domain
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "name": name,
                "base_url": base_url,
                "client_id": client_id,
                "secret": secret,
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

        name = d.pop("name")

        base_url = d.pop("base_url")

        client_id = d.pop("client_id")

        secret = d.pop("secret")

        domain = d.pop("domain", UNSET)

        enabled = d.pop("enabled", UNSET)

        git_lab_auth_provider_model_auth_provider = cls(
            id=id,
            type=type,
            name=name,
            base_url=base_url,
            client_id=client_id,
            secret=secret,
            domain=domain,
            enabled=enabled,
        )

        git_lab_auth_provider_model_auth_provider.additional_properties = d
        return git_lab_auth_provider_model_auth_provider

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
