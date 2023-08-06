from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_token_update_permissions import PatchedTokenUpdatePermissions


T = TypeVar("T", bound="PatchedTokenUpdate")


@attr.s(auto_attribs=True)
class PatchedTokenUpdate:
    """
    Attributes:
        name (Union[Unset, str]): The human readable name of the database token for the user.
        permissions (Union[Unset, PatchedTokenUpdatePermissions]): Indicates per operation which permissions the
            database token has within the whole workspace. If the value of for example `create` is `true`, then the token
            can create rows in all tables related to the workspace. If a list is provided with for example `[["table", 1]]`
            then the token only has create permissions for the table with id 1. Same goes for if a database references is
            provided. `[['database', 1]]` means create permissions for all tables in the database with id 1.

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
        rotate_key (Union[Unset, bool]): Indicates if a new key must be generated.
    """

    name: Union[Unset, str] = UNSET
    permissions: Union[Unset, "PatchedTokenUpdatePermissions"] = UNSET
    rotate_key: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        permissions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions.to_dict()

        rotate_key = self.rotate_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if rotate_key is not UNSET:
            field_dict["rotate_key"] = rotate_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patched_token_update_permissions import PatchedTokenUpdatePermissions

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _permissions = d.pop("permissions", UNSET)
        permissions: Union[Unset, PatchedTokenUpdatePermissions]
        if isinstance(_permissions, Unset):
            permissions = UNSET
        else:
            permissions = PatchedTokenUpdatePermissions.from_dict(_permissions)

        rotate_key = d.pop("rotate_key", UNSET)

        patched_token_update = cls(
            name=name,
            permissions=permissions,
            rotate_key=rotate_key,
        )

        patched_token_update.additional_properties = d
        return patched_token_update

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
