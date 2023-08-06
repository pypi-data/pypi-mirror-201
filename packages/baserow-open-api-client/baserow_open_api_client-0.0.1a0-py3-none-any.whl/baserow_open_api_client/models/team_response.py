import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_sample_subject import TeamSampleSubject


T = TypeVar("T", bound="TeamResponse")


@attr.s(auto_attribs=True)
class TeamResponse:
    """
    Attributes:
        id (int):
        name (str): A human friendly name for this team.
        group (int): DEPRECATED: Please use the functionally identical `workspace` instead as this field is being
            removed in the future.
        workspace (int): The workspace that this team belongs to.
        created_on (datetime.datetime):
        updated_on (datetime.datetime):
        subject_count (int): The amount of subjects (e.g. users) that are currently assigned to this team.
        default_role (Union[Unset, str]): The uid of the role this team has in its workspace.
        subject_sample (Union[Unset, List['TeamSampleSubject']]): A sample, by default 10, of the most recent subjects
            to join this team.
    """

    id: int
    name: str
    group: int
    workspace: int
    created_on: datetime.datetime
    updated_on: datetime.datetime
    subject_count: int
    default_role: Union[Unset, str] = UNSET
    subject_sample: Union[Unset, List["TeamSampleSubject"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        group = self.group
        workspace = self.workspace
        created_on = self.created_on.isoformat()

        updated_on = self.updated_on.isoformat()

        subject_count = self.subject_count
        default_role = self.default_role
        subject_sample: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subject_sample, Unset):
            subject_sample = []
            for subject_sample_item_data in self.subject_sample:
                subject_sample_item = subject_sample_item_data.to_dict()

                subject_sample.append(subject_sample_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "group": group,
                "workspace": workspace,
                "created_on": created_on,
                "updated_on": updated_on,
                "subject_count": subject_count,
            }
        )
        if default_role is not UNSET:
            field_dict["default_role"] = default_role
        if subject_sample is not UNSET:
            field_dict["subject_sample"] = subject_sample

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.team_sample_subject import TeamSampleSubject

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        group = d.pop("group")

        workspace = d.pop("workspace")

        created_on = isoparse(d.pop("created_on"))

        updated_on = isoparse(d.pop("updated_on"))

        subject_count = d.pop("subject_count")

        default_role = d.pop("default_role", UNSET)

        subject_sample = []
        _subject_sample = d.pop("subject_sample", UNSET)
        for subject_sample_item_data in _subject_sample or []:
            subject_sample_item = TeamSampleSubject.from_dict(subject_sample_item_data)

            subject_sample.append(subject_sample_item)

        team_response = cls(
            id=id,
            name=name,
            group=group,
            workspace=workspace,
            created_on=created_on,
            updated_on=updated_on,
            subject_count=subject_count,
            default_role=default_role,
            subject_sample=subject_sample,
        )

        team_response.additional_properties = d
        return team_response

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
