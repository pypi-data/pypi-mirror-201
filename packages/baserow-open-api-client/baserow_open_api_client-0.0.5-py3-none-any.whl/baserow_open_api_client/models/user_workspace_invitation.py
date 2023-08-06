import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="UserWorkspaceInvitation")


@attr.s(auto_attribs=True)
class UserWorkspaceInvitation:
    """This serializer is used for displaying the invitation to the user that doesn't
    have access to the workspace yet, so not for invitation management purposes.

        Attributes:
            id (int):
            invited_by (str):
            group (str):
            workspace (str):
            email (str): The email address of the user that the invitation is meant for. Only a user with that email address
                can accept it.
            message (str): An optional message that the invitor can provide. This will be visible to the receiver of the
                invitation.
            created_on (datetime.datetime):
            email_exists (bool):
    """

    id: int
    invited_by: str
    group: str
    workspace: str
    email: str
    message: str
    created_on: datetime.datetime
    email_exists: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        invited_by = self.invited_by
        group = self.group
        workspace = self.workspace
        email = self.email
        message = self.message
        created_on = self.created_on.isoformat()

        email_exists = self.email_exists

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "invited_by": invited_by,
                "group": group,
                "workspace": workspace,
                "email": email,
                "message": message,
                "created_on": created_on,
                "email_exists": email_exists,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        invited_by = d.pop("invited_by")

        group = d.pop("group")

        workspace = d.pop("workspace")

        email = d.pop("email")

        message = d.pop("message")

        created_on = isoparse(d.pop("created_on"))

        email_exists = d.pop("email_exists")

        user_workspace_invitation = cls(
            id=id,
            invited_by=invited_by,
            group=group,
            workspace=workspace,
            email=email,
            message=message,
            created_on=created_on,
            email_exists=email_exists,
        )

        user_workspace_invitation.additional_properties = d
        return user_workspace_invitation

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
