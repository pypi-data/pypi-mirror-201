import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_user_enterprise_team import WorkspaceUserEnterpriseTeam


T = TypeVar("T", bound="ListWorkspaceUsersWithMemberData")


@attr.s(auto_attribs=True)
class ListWorkspaceUsersWithMemberData:
    """Mixin to a DRF serializer class to raise an exception if data with unknown fields
    is provided to the serializer.

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
            teams (Union[Unset, List['WorkspaceUserEnterpriseTeam']]): Enterprise only: a list of team IDs and names, which
                this workspace user belongs to in this workspace.
            role_uid (Union[Unset, None, str]): Enterprise or advanced only: the uid of the role that is assigned to this
                workspace user in this workspace.
            highest_role_uid (Union[Unset, None, str]): Enterprise or advanced only: the highest role uid assigned to this
                user in this workspace on anything, including roles from teams.
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
    teams: Union[Unset, List["WorkspaceUserEnterpriseTeam"]] = UNSET
    role_uid: Union[Unset, None, str] = UNSET
    highest_role_uid: Union[Unset, None, str] = UNSET
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
        teams: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.teams, Unset):
            teams = []
            for teams_item_data in self.teams:
                teams_item = teams_item_data.to_dict()

                teams.append(teams_item)

        role_uid = self.role_uid
        highest_role_uid = self.highest_role_uid

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
        if teams is not UNSET:
            field_dict["teams"] = teams
        if role_uid is not UNSET:
            field_dict["role_uid"] = role_uid
        if highest_role_uid is not UNSET:
            field_dict["highest_role_uid"] = highest_role_uid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_user_enterprise_team import WorkspaceUserEnterpriseTeam

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

        teams = []
        _teams = d.pop("teams", UNSET)
        for teams_item_data in _teams or []:
            teams_item = WorkspaceUserEnterpriseTeam.from_dict(teams_item_data)

            teams.append(teams_item)

        role_uid = d.pop("role_uid", UNSET)

        highest_role_uid = d.pop("highest_role_uid", UNSET)

        list_workspace_users_with_member_data = cls(
            id=id,
            name=name,
            email=email,
            group=group,
            workspace=workspace,
            created_on=created_on,
            user_id=user_id,
            to_be_deleted=to_be_deleted,
            permissions=permissions,
            teams=teams,
            role_uid=role_uid,
            highest_role_uid=highest_role_uid,
        )

        list_workspace_users_with_member_data.additional_properties = d
        return list_workspace_users_with_member_data

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
