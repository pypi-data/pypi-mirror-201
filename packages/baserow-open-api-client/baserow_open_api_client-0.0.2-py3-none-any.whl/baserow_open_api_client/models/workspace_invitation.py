import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceInvitation")


@attr.s(auto_attribs=True)
class WorkspaceInvitation:
    """
    Attributes:
        id (int):
        group (int): DEPRECATED: Please use the functionally identical `workspace` instead as this field is being
            removed in the future.
        workspace (int): The workspace that the user will get access to once the invitation is accepted.
        email (str): The email address of the user that the invitation is meant for. Only a user with that email address
            can accept it.
        created_on (datetime.datetime):
        permissions (Union[Unset, str]): The permissions that the user is going to get within the workspace after
            accepting the invitation.
        message (Union[Unset, str]): An optional message that the invitor can provide. This will be visible to the
            receiver of the invitation.
    """

    id: int
    group: int
    workspace: int
    email: str
    created_on: datetime.datetime
    permissions: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        group = self.group
        workspace = self.workspace
        email = self.email
        created_on = self.created_on.isoformat()

        permissions = self.permissions
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "group": group,
                "workspace": workspace,
                "email": email,
                "created_on": created_on,
            }
        )
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        group = d.pop("group")

        workspace = d.pop("workspace")

        email = d.pop("email")

        created_on = isoparse(d.pop("created_on"))

        permissions = d.pop("permissions", UNSET)

        message = d.pop("message", UNSET)

        workspace_invitation = cls(
            id=id,
            group=group,
            workspace=workspace,
            email=email,
            created_on=created_on,
            permissions=permissions,
            message=message,
        )

        workspace_invitation.additional_properties = d
        return workspace_invitation

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
