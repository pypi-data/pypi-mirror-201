from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.user_workspace_invitation import UserWorkspaceInvitation


T = TypeVar("T", bound="Dashboard")


@attr.s(auto_attribs=True)
class Dashboard:
    """
    Attributes:
        group_invitations (List['UserWorkspaceInvitation']):
        workspace_invitations (List['UserWorkspaceInvitation']):
    """

    group_invitations: List["UserWorkspaceInvitation"]
    workspace_invitations: List["UserWorkspaceInvitation"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        group_invitations = []
        for group_invitations_item_data in self.group_invitations:
            group_invitations_item = group_invitations_item_data.to_dict()

            group_invitations.append(group_invitations_item)

        workspace_invitations = []
        for workspace_invitations_item_data in self.workspace_invitations:
            workspace_invitations_item = workspace_invitations_item_data.to_dict()

            workspace_invitations.append(workspace_invitations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_invitations": group_invitations,
                "workspace_invitations": workspace_invitations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_workspace_invitation import UserWorkspaceInvitation

        d = src_dict.copy()
        group_invitations = []
        _group_invitations = d.pop("group_invitations")
        for group_invitations_item_data in _group_invitations:
            group_invitations_item = UserWorkspaceInvitation.from_dict(group_invitations_item_data)

            group_invitations.append(group_invitations_item)

        workspace_invitations = []
        _workspace_invitations = d.pop("workspace_invitations")
        for workspace_invitations_item_data in _workspace_invitations:
            workspace_invitations_item = UserWorkspaceInvitation.from_dict(workspace_invitations_item_data)

            workspace_invitations.append(workspace_invitations_item)

        dashboard = cls(
            group_invitations=group_invitations,
            workspace_invitations=workspace_invitations,
        )

        dashboard.additional_properties = d
        return dashboard

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
