from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.subject_type_3_ff_enum import SubjectType3FfEnum

T = TypeVar("T", bound="TeamSampleSubject")


@attr.s(auto_attribs=True)
class TeamSampleSubject:
    """
    Attributes:
        subject_id (int): The subject's unique identifier.
        subject_type (SubjectType3FfEnum):
        subject_label (str): The subject's label. Defaults to a user's first name.
        team_subject_id (int): The team subject unique identifier.
    """

    subject_id: int
    subject_type: SubjectType3FfEnum
    subject_label: str
    team_subject_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject_id = self.subject_id
        subject_type = self.subject_type.value

        subject_label = self.subject_label
        team_subject_id = self.team_subject_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subject_id": subject_id,
                "subject_type": subject_type,
                "subject_label": subject_label,
                "team_subject_id": team_subject_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject_id = d.pop("subject_id")

        subject_type = SubjectType3FfEnum(d.pop("subject_type"))

        subject_label = d.pop("subject_label")

        team_subject_id = d.pop("team_subject_id")

        team_sample_subject = cls(
            subject_id=subject_id,
            subject_type=subject_type,
            subject_label=subject_label,
            team_subject_id=team_subject_id,
        )

        team_sample_subject.additional_properties = d
        return team_sample_subject

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
