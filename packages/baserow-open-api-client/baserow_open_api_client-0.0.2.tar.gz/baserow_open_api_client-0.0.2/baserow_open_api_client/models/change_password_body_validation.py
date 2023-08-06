from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ChangePasswordBodyValidation")


@attr.s(auto_attribs=True)
class ChangePasswordBodyValidation:
    """
    Attributes:
        old_password (str):
        new_password (str):
    """

    old_password: str
    new_password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        old_password = self.old_password
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "old_password": old_password,
                "new_password": new_password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        old_password = d.pop("old_password")

        new_password = d.pop("new_password")

        change_password_body_validation = cls(
            old_password=old_password,
            new_password=new_password,
        )

        change_password_body_validation.additional_properties = d
        return change_password_body_validation

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
