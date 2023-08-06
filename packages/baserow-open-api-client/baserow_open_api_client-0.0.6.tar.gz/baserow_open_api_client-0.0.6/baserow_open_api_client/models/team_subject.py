from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.subject_type_3_ff_enum import SubjectType3FfEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="TeamSubject")


@attr.s(auto_attribs=True)
class TeamSubject:
    """Mixin to a DRF serializer class to raise an exception if data with unknown fields
    is provided to the serializer.

        Attributes:
            id (int):
            subject_type (SubjectType3FfEnum):
            subject_id (Union[Unset, int]): The subject's unique identifier.
            subject_user_email (Union[Unset, str]): The user subject's email address.
    """

    id: int
    subject_type: SubjectType3FfEnum
    subject_id: Union[Unset, int] = UNSET
    subject_user_email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        subject_type = self.subject_type.value

        subject_id = self.subject_id
        subject_user_email = self.subject_user_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "subject_type": subject_type,
            }
        )
        if subject_id is not UNSET:
            field_dict["subject_id"] = subject_id
        if subject_user_email is not UNSET:
            field_dict["subject_user_email"] = subject_user_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        subject_type = SubjectType3FfEnum(d.pop("subject_type"))

        subject_id = d.pop("subject_id", UNSET)

        subject_user_email = d.pop("subject_user_email", UNSET)

        team_subject = cls(
            id=id,
            subject_type=subject_type,
            subject_id=subject_id,
            subject_user_email=subject_user_email,
        )

        team_subject.additional_properties = d
        return team_subject

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
