from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.token_permissions import TokenPermissions


T = TypeVar("T", bound="Token")


@attr.s(auto_attribs=True)
class Token:
    """A mixin that allows us to rename the `group` field to `workspace` when serializing.

    Attributes:
        id (int):
        name (str): The human readable name of the database token for the user.
        group (str):
        workspace (int): Only the tables of the workspace can be accessed.
        key (str): The unique token key that can be used to authorize for the table row endpoints.
        permissions (TokenPermissions): Indicates per operation which permissions the database token has within the
            whole workspace. If the value of for example `create` is `true`, then the token can create rows in all tables
            related to the workspace. If a list is provided with for example `[["table", 1]]` then the token only has create
            permissions for the table with id 1. Same goes for if a database references is provided. `[['database', 1]]`
            means create permissions for all tables in the database with id 1.

            Example:
            ```json
            {
              "create": true// Allows creating rows in all tables.
              // Allows reading rows from database 1 and table 10.
              "read": [["database", 1], ["table", 10]],
              "update": false  // Denies updating rows in all tables.
              "delete": []  // Denies deleting rows in all tables.
             }
            ```
    """

    id: int
    name: str
    group: str
    workspace: int
    key: str
    permissions: "TokenPermissions"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        group = self.group
        workspace = self.workspace
        key = self.key
        permissions = self.permissions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "group": group,
                "workspace": workspace,
                "key": key,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_permissions import TokenPermissions

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        group = d.pop("group")

        workspace = d.pop("workspace")

        key = d.pop("key")

        permissions = TokenPermissions.from_dict(d.pop("permissions"))

        token = cls(
            id=id,
            name=name,
            group=group,
            workspace=workspace,
            key=key,
            permissions=permissions,
        )

        token.additional_properties = d
        return token

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
