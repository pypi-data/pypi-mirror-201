import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_admin_groups import UserAdminGroups


T = TypeVar("T", bound="UserAdminResponse")


@attr.s(auto_attribs=True)
class UserAdminResponse:
    """Serializes the safe user attributes to expose for a response back to the user.

    Attributes:
        id (int):
        username (str):
        name (str):
        groups (List['UserAdminGroups']):
        workspaces (List['UserAdminGroups']):
        last_login (Union[Unset, None, datetime.datetime]):
        date_joined (Union[Unset, datetime.datetime]):
        is_active (Union[Unset, bool]): Designates whether this user should be treated as active. Set this to false
            instead of deleting accounts.
        is_staff (Union[Unset, bool]): Designates whether this user is an admin and has access to all workspaces and
            Baserow's admin areas.
    """

    id: int
    username: str
    name: str
    groups: List["UserAdminGroups"]
    workspaces: List["UserAdminGroups"]
    last_login: Union[Unset, None, datetime.datetime] = UNSET
    date_joined: Union[Unset, datetime.datetime] = UNSET
    is_active: Union[Unset, bool] = UNSET
    is_staff: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        username = self.username
        name = self.name
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()

            groups.append(groups_item)

        workspaces = []
        for workspaces_item_data in self.workspaces:
            workspaces_item = workspaces_item_data.to_dict()

            workspaces.append(workspaces_item)

        last_login: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_login, Unset):
            last_login = self.last_login.isoformat() if self.last_login else None

        date_joined: Union[Unset, str] = UNSET
        if not isinstance(self.date_joined, Unset):
            date_joined = self.date_joined.isoformat()

        is_active = self.is_active
        is_staff = self.is_staff

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "username": username,
                "name": name,
                "groups": groups,
                "workspaces": workspaces,
            }
        )
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if date_joined is not UNSET:
            field_dict["date_joined"] = date_joined
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_admin_groups import UserAdminGroups

        d = src_dict.copy()
        id = d.pop("id")

        username = d.pop("username")

        name = d.pop("name")

        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = UserAdminGroups.from_dict(groups_item_data)

            groups.append(groups_item)

        workspaces = []
        _workspaces = d.pop("workspaces")
        for workspaces_item_data in _workspaces:
            workspaces_item = UserAdminGroups.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        _last_login = d.pop("last_login", UNSET)
        last_login: Union[Unset, None, datetime.datetime]
        if _last_login is None:
            last_login = None
        elif isinstance(_last_login, Unset):
            last_login = UNSET
        else:
            last_login = isoparse(_last_login)

        _date_joined = d.pop("date_joined", UNSET)
        date_joined: Union[Unset, datetime.datetime]
        if isinstance(_date_joined, Unset):
            date_joined = UNSET
        else:
            date_joined = isoparse(_date_joined)

        is_active = d.pop("is_active", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        user_admin_response = cls(
            id=id,
            username=username,
            name=name,
            groups=groups,
            workspaces=workspaces,
            last_login=last_login,
            date_joined=date_joined,
            is_active=is_active,
            is_staff=is_staff,
        )

        user_admin_response.additional_properties = d
        return user_admin_response

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
