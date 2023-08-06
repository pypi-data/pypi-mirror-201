from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SendResetPasswordEmailBodyValidation")


@attr.s(auto_attribs=True)
class SendResetPasswordEmailBodyValidation:
    """
    Attributes:
        email (str): The email address of the user that has requested a password reset.
        base_url (str): The base URL where the user can reset his password. The reset token is going to be appended to
            the base_url (base_url '/token').
    """

    email: str
    base_url: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        base_url = self.base_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "base_url": base_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        base_url = d.pop("base_url")

        send_reset_password_email_body_validation = cls(
            email=email,
            base_url=base_url,
        )

        send_reset_password_email_body_validation.additional_properties = d
        return send_reset_password_email_body_validation

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
