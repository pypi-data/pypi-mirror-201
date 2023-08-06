from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.permission_object_permissions import PermissionObjectPermissions


T = TypeVar("T", bound="PermissionObject")


@attr.s(auto_attribs=True)
class PermissionObject:
    """
    Attributes:
        name (str): The permission manager name.
        permissions (PermissionObjectPermissions): The content of the permission object for this permission manager.
    """

    name: str
    permissions: "PermissionObjectPermissions"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        permissions = self.permissions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.permission_object_permissions import PermissionObjectPermissions

        d = src_dict.copy()
        name = d.pop("name")

        permissions = PermissionObjectPermissions.from_dict(d.pop("permissions"))

        permission_object = cls(
            name=name,
            permissions=permissions,
        )

        permission_object.additional_properties = d
        return permission_object

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
