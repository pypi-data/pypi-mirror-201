from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspaceInvitation")


@attr.s(auto_attribs=True)
class CreateWorkspaceInvitation:
    """
    Attributes:
        email (str): The email address of the user that the invitation is meant for. Only a user with that email address
            can accept it.
        base_url (str): The base URL where the user can publicly accept his invitation.The accept token is going to be
            appended to the base_url (base_url '/token').
        permissions (Union[Unset, str]): The permissions that the user is going to get within the workspace after
            accepting the invitation.
        message (Union[Unset, str]): An optional message that the invitor can provide. This will be visible to the
            receiver of the invitation.
    """

    email: str
    base_url: str
    permissions: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        base_url = self.base_url
        permissions = self.permissions
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "base_url": base_url,
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
        email = d.pop("email")

        base_url = d.pop("base_url")

        permissions = d.pop("permissions", UNSET)

        message = d.pop("message", UNSET)

        create_workspace_invitation = cls(
            email=email,
            base_url=base_url,
            permissions=permissions,
            message=message,
        )

        create_workspace_invitation.additional_properties = d
        return create_workspace_invitation

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
