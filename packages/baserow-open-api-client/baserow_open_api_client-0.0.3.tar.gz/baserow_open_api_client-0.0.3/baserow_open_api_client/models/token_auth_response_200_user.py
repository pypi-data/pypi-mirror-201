from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenAuthResponse200User")


@attr.s(auto_attribs=True)
class TokenAuthResponse200User:
    """An object containing information related to the user.

    Attributes:
        first_name (Union[Unset, str]): The first name of related user.
        username (Union[Unset, str]): The username of the related user. This is always an email address.
        language (Union[Unset, str]): An ISO 639 language code (with optional variant) selected by the user. Ex: en-GB.
    """

    first_name: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        username = self.username
        language = self.language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if username is not UNSET:
            field_dict["username"] = username
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("first_name", UNSET)

        username = d.pop("username", UNSET)

        language = d.pop("language", UNSET)

        token_auth_response_200_user = cls(
            first_name=first_name,
            username=username,
            language=language,
        )

        token_auth_response_200_user.additional_properties = d
        return token_auth_response_200_user

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
