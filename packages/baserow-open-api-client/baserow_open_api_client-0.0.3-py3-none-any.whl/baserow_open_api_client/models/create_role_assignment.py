from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

from ..models.scope_type_enum import ScopeTypeEnum
from ..models.subject_type_6_dc_enum import SubjectType6DcEnum

T = TypeVar("T", bound="CreateRoleAssignment")


@attr.s(auto_attribs=True)
class CreateRoleAssignment:
    """The create role assignment serializer.

    Attributes:
        subject_id (int): The subject ID. A subject is an actor that can do operations.
        subject_type (SubjectType6DcEnum):
        scope_id (int): The ID of the scope object. The scope object limit the role assignment to this scope and all its
            descendants.
        scope_type (ScopeTypeEnum):
        role (Optional[str]): The uid of the role you want to assign to the user or team in the given workspace. You can
            omit this property if you want to remove the role.
    """

    subject_id: int
    subject_type: SubjectType6DcEnum
    scope_id: int
    scope_type: ScopeTypeEnum
    role: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_id = self.subject_id
        subject_type = self.subject_type.value

        scope_id = self.scope_id
        scope_type = self.scope_type.value

        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subject_id": subject_id,
                "subject_type": subject_type,
                "scope_id": scope_id,
                "scope_type": scope_type,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject_id = d.pop("subject_id")

        subject_type = SubjectType6DcEnum(d.pop("subject_type"))

        scope_id = d.pop("scope_id")

        scope_type = ScopeTypeEnum(d.pop("scope_type"))

        role = d.pop("role")

        create_role_assignment = cls(
            subject_id=subject_id,
            subject_type=subject_type,
            scope_id=scope_id,
            scope_type=scope_type,
            role=role,
        )

        create_role_assignment.additional_properties = d
        return create_role_assignment

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
