from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenRefreshWithUser")


@attr.s(auto_attribs=True)
class TokenRefreshWithUser:
    """
    Attributes:
        access (str):
        refresh_token (Union[Unset, str]):
        token (Union[Unset, str]): Deprecated. Use `refresh_token` instead.
    """

    access: str
    refresh_token: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access = self.access
        refresh_token = self.refresh_token
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access": access,
            }
        )
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access = d.pop("access")

        refresh_token = d.pop("refresh_token", UNSET)

        token = d.pop("token", UNSET)

        token_refresh_with_user = cls(
            access=access,
            refresh_token=refresh_token,
            token=token,
        )

        token_refresh_with_user.additional_properties = d
        return token_refresh_with_user

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
