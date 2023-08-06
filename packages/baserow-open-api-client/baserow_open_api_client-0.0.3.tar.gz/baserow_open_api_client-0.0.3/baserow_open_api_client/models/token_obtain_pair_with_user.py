from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenObtainPairWithUser")


@attr.s(auto_attribs=True)
class TokenObtainPairWithUser:
    """
    Attributes:
        password (str):
        email (Union[Unset, str]):
        username (Union[Unset, str]): Deprecated. Use `email` instead.
    """

    password: str
    email: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        password = self.password
        email = self.email
        username = self.username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "password": password,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        password = d.pop("password")

        email = d.pop("email", UNSET)

        username = d.pop("username", UNSET)

        token_obtain_pair_with_user = cls(
            password=password,
            email=email,
            username=username,
        )

        token_obtain_pair_with_user.additional_properties = d
        return token_obtain_pair_with_user

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
