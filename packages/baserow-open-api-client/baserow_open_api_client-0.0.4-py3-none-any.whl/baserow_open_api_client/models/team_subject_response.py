from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TeamSubjectResponse")


@attr.s(auto_attribs=True)
class TeamSubjectResponse:
    """
    Attributes:
        id (int):
        subject_id (int): The unique subject ID.
        subject_type (str):
        team (int): The team this subject belongs to.
    """

    id: int
    subject_id: int
    subject_type: str
    team: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        subject_id = self.subject_id
        subject_type = self.subject_type
        team = self.team

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "subject_id": subject_id,
                "subject_type": subject_type,
                "team": team,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        subject_id = d.pop("subject_id")

        subject_type = d.pop("subject_type")

        team = d.pop("team")

        team_subject_response = cls(
            id=id,
            subject_id=subject_id,
            subject_type=subject_type,
            team=team,
        )

        team_subject_response.additional_properties = d
        return team_subject_response

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
