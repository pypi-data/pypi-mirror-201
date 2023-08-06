import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceUser")


@attr.s(auto_attribs=True)
class WorkspaceUser:
    """
    Attributes:
        id (int):
        name (str): User defined name.
        email (str): User email.
        group (int): DEPRECATED: Please use the functionally identical `workspace` instead as this field is being
            removed in the future.
        workspace (int): The workspace that the user has access to.
        created_on (datetime.datetime):
        user_id (int): The user that has access to the workspace.
        to_be_deleted (bool): True if user account is pending deletion.
        permissions (Union[Unset, str]): The permissions that the user has within the workspace.
    """

    id: int
    name: str
    email: str
    group: int
    workspace: int
    created_on: datetime.datetime
    user_id: int
    to_be_deleted: bool
    permissions: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        email = self.email
        group = self.group
        workspace = self.workspace
        created_on = self.created_on.isoformat()

        user_id = self.user_id
        to_be_deleted = self.to_be_deleted
        permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "email": email,
                "group": group,
                "workspace": workspace,
                "created_on": created_on,
                "user_id": user_id,
                "to_be_deleted": to_be_deleted,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        email = d.pop("email")

        group = d.pop("group")

        workspace = d.pop("workspace")

        created_on = isoparse(d.pop("created_on"))

        user_id = d.pop("user_id")

        to_be_deleted = d.pop("to_be_deleted")

        permissions = d.pop("permissions", UNSET)

        workspace_user = cls(
            id=id,
            name=name,
            email=email,
            group=group,
            workspace=workspace,
            created_on=created_on,
            user_id=user_id,
            to_be_deleted=to_be_deleted,
            permissions=permissions,
        )

        workspace_user.additional_properties = d
        return workspace_user

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
