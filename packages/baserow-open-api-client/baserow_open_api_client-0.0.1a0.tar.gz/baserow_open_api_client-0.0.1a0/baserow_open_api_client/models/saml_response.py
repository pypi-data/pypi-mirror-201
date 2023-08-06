from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SAMLResponse")


@attr.s(auto_attribs=True)
class SAMLResponse:
    """
    Attributes:
        saml_response (str): The encoded SAML response from the IdP.
        relay_state (str): The frontend URL where redirect the authenticated user.
    """

    saml_response: str
    relay_state: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        saml_response = self.saml_response
        relay_state = self.relay_state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "SAMLResponse": saml_response,
                "RelayState": relay_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        saml_response = d.pop("SAMLResponse")

        relay_state = d.pop("RelayState")

        saml_response = cls(
            saml_response=saml_response,
            relay_state=relay_state,
        )

        saml_response.additional_properties = d
        return saml_response

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
