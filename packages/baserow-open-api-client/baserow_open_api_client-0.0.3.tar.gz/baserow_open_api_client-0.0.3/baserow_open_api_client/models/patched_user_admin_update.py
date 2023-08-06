from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUserAdminUpdate")


@attr.s(auto_attribs=True)
class PatchedUserAdminUpdate:
    """Serializes a request body for updating a given user. Do not use for returning user
    data as the password will be returned also.

        Attributes:
            username (Union[Unset, str]):
            name (Union[Unset, str]):
            is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Set this to false
                instead of deleting accounts.
            is_staff (Union[Unset, bool]): Designates whether this user is an admin and has access to all workspaces and
                Baserow's admin areas.
            password (Union[Unset, str]):
    """

    username: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    is_staff: Union[Unset, bool] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        name = self.name
        is_active = self.is_active
        is_staff = self.is_staff
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if name is not UNSET:
            field_dict["name"] = name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", UNSET)

        name = d.pop("name", UNSET)

        is_active = d.pop("is_active", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        password = d.pop("password", UNSET)

        patched_user_admin_update = cls(
            username=username,
            name=name,
            is_active=is_active,
            is_staff=is_staff,
            password=password,
        )

        patched_user_admin_update.additional_properties = d
        return patched_user_admin_update

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
