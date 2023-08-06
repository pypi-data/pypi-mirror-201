from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_verify_response_200_user import TokenVerifyResponse200User


T = TypeVar("T", bound="TokenVerifyResponse200")


@attr.s(auto_attribs=True)
class TokenVerifyResponse200:
    """
    Attributes:
        user (Union[Unset, TokenVerifyResponse200User]): An object containing information related to the user.
    """

    user: Union[Unset, "TokenVerifyResponse200User"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_verify_response_200_user import TokenVerifyResponse200User

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, TokenVerifyResponse200User]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = TokenVerifyResponse200User.from_dict(_user)

        token_verify_response_200 = cls(
            user=user,
        )

        token_verify_response_200.additional_properties = d
        return token_verify_response_200

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
