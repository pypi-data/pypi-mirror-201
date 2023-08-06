import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_admin_users import WorkspaceAdminUsers


T = TypeVar("T", bound="WorkspacesAdminResponse")


@attr.s(auto_attribs=True)
class WorkspacesAdminResponse:
    """
    Attributes:
        id (int):
        name (str):
        users (List['WorkspaceAdminUsers']):
        application_count (int):
        row_count (int):
        seats_taken (int):
        free_users (int):
        created_on (datetime.datetime):
        storage_usage (Union[Unset, None, int]):
    """

    id: int
    name: str
    users: List["WorkspaceAdminUsers"]
    application_count: int
    row_count: int
    seats_taken: int
    free_users: int
    created_on: datetime.datetime
    storage_usage: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()

            users.append(users_item)

        application_count = self.application_count
        row_count = self.row_count
        seats_taken = self.seats_taken
        free_users = self.free_users
        created_on = self.created_on.isoformat()

        storage_usage = self.storage_usage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "users": users,
                "application_count": application_count,
                "row_count": row_count,
                "seats_taken": seats_taken,
                "free_users": free_users,
                "created_on": created_on,
            }
        )
        if storage_usage is not UNSET:
            field_dict["storage_usage"] = storage_usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_admin_users import WorkspaceAdminUsers

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = WorkspaceAdminUsers.from_dict(users_item_data)

            users.append(users_item)

        application_count = d.pop("application_count")

        row_count = d.pop("row_count")

        seats_taken = d.pop("seats_taken")

        free_users = d.pop("free_users")

        created_on = isoparse(d.pop("created_on"))

        storage_usage = d.pop("storage_usage", UNSET)

        workspaces_admin_response = cls(
            id=id,
            name=name,
            users=users,
            application_count=application_count,
            row_count=row_count,
            seats_taken=seats_taken,
            free_users=free_users,
            created_on=created_on,
            storage_usage=storage_usage,
        )

        workspaces_admin_response.additional_properties = d
        return workspaces_admin_response

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
