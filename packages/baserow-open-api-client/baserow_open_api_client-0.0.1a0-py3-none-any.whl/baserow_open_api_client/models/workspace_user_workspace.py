from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.workspace_user import WorkspaceUser


T = TypeVar("T", bound="WorkspaceUserWorkspace")


@attr.s(auto_attribs=True)
class WorkspaceUserWorkspace:
    """This serializers includes relevant fields of the Workspace model, but also
    some WorkspaceUser specific fields related to the workspace user relation.

    Additionally, the list of users are included for each workspace.

        Attributes:
            id (int): Workspace id.
            name (str): Workspace name.
            users (List['WorkspaceUser']): List of all workspace users.
            order (int): The requesting user's order within the workspace users.
            permissions (str): The requesting user's permissions for the workspace.
    """

    id: int
    name: str
    users: List["WorkspaceUser"]
    order: int
    permissions: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()

            users.append(users_item)

        order = self.order
        permissions = self.permissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "users": users,
                "order": order,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_user import WorkspaceUser

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = WorkspaceUser.from_dict(users_item_data)

            users.append(users_item)

        order = d.pop("order")

        permissions = d.pop("permissions")

        workspace_user_workspace = cls(
            id=id,
            name=name,
            users=users,
            order=order,
            permissions=permissions,
        )

        workspace_user_workspace.additional_properties = d
        return workspace_user_workspace

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
