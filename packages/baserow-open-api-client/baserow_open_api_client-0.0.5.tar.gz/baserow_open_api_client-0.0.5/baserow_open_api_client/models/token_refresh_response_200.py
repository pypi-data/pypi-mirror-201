from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_refresh_response_200_user import TokenRefreshResponse200User


T = TypeVar("T", bound="TokenRefreshResponse200")


@attr.s(auto_attribs=True)
class TokenRefreshResponse200:
    """
    Attributes:
        user (Union[Unset, TokenRefreshResponse200User]): An object containing information related to the user.
        token (Union[Unset, str]): Deprecated. Use the `access_token` instead.
        access_token (Union[Unset, str]): 'access_token' can be used to authorize for other endpoints that require
            authorization. This token will be valid for 10 minutes.
    """

    user: Union[Unset, "TokenRefreshResponse200User"] = UNSET
    token: Union[Unset, str] = UNSET
    access_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        token = self.token
        access_token = self.access_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if token is not UNSET:
            field_dict["token"] = token
        if access_token is not UNSET:
            field_dict["access_token"] = access_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_refresh_response_200_user import TokenRefreshResponse200User

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, TokenRefreshResponse200User]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = TokenRefreshResponse200User.from_dict(_user)

        token = d.pop("token", UNSET)

        access_token = d.pop("access_token", UNSET)

        token_refresh_response_200 = cls(
            user=user,
            token=token,
            access_token=access_token,
        )

        token_refresh_response_200.additional_properties = d
        return token_refresh_response_200

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
