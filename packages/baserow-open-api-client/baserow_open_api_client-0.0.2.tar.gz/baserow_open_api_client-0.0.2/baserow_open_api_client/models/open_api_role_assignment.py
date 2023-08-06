from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.scope_type_enum import ScopeTypeEnum
from ..models.subject_type_6_dc_enum import SubjectType6DcEnum

if TYPE_CHECKING:
    from ..models.open_api_subject_field import OpenApiSubjectField


T = TypeVar("T", bound="OpenApiRoleAssignment")


@attr.s(auto_attribs=True)
class OpenApiRoleAssignment:
    """Serializer for RoleAssignment used for the Open API spec

    Attributes:
        id (int):
        role (str): The uid of the role assigned to the user or team in the given workspace.
        subject (OpenApiSubjectField):
        subject_id (int): The subject ID.
        scope_id (int): The unique scope ID.
        subject_type (SubjectType6DcEnum):
        scope_type (ScopeTypeEnum):
    """

    id: int
    role: str
    subject: "OpenApiSubjectField"
    subject_id: int
    scope_id: int
    subject_type: SubjectType6DcEnum
    scope_type: ScopeTypeEnum
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        role = self.role
        subject = self.subject.to_dict()

        subject_id = self.subject_id
        scope_id = self.scope_id
        subject_type = self.subject_type.value

        scope_type = self.scope_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "role": role,
                "subject": subject,
                "subject_id": subject_id,
                "scope_id": scope_id,
                "subject_type": subject_type,
                "scope_type": scope_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.open_api_subject_field import OpenApiSubjectField

        d = src_dict.copy()
        id = d.pop("id")

        role = d.pop("role")

        subject = OpenApiSubjectField.from_dict(d.pop("subject"))

        subject_id = d.pop("subject_id")

        scope_id = d.pop("scope_id")

        subject_type = SubjectType6DcEnum(d.pop("subject_type"))

        scope_type = ScopeTypeEnum(d.pop("scope_type"))

        open_api_role_assignment = cls(
            id=id,
            role=role,
            subject=subject,
            subject_id=subject_id,
            scope_id=scope_id,
            subject_type=subject_type,
            scope_type=scope_type,
        )

        open_api_role_assignment.additional_properties = d
        return open_api_role_assignment

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
