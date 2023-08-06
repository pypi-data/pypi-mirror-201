from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUpdateWorkspaceInvitation")


@attr.s(auto_attribs=True)
class PatchedUpdateWorkspaceInvitation:
    """
    Attributes:
        permissions (Union[Unset, str]): The permissions that the user is going to get within the workspace after
            accepting the invitation.
    """

    permissions: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        permissions = d.pop("permissions", UNSET)

        patched_update_workspace_invitation = cls(
            permissions=permissions,
        )

        patched_update_workspace_invitation.additional_properties = d
        return patched_update_workspace_invitation

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
