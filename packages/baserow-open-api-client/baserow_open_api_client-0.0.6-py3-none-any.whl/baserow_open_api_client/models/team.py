from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.team_subject import TeamSubject


T = TypeVar("T", bound="Team")


@attr.s(auto_attribs=True)
class Team:
    """Mixin to a DRF serializer class to raise an exception if data with unknown fields
    is provided to the serializer.

        Attributes:
            name (str): A human friendly name for this team.
            default_role (Union[Unset, None, str]): The uid of the role you want to assign to the team in the given
                workspace. You can omit this property if you want to remove the role.
            subjects (Union[Unset, List['TeamSubject']]): An array of subject ID/type objects to be used during team create
                and update.
    """

    name: str
    default_role: Union[Unset, None, str] = UNSET
    subjects: Union[Unset, List["TeamSubject"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        default_role = self.default_role
        subjects: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subjects, Unset):
            subjects = []
            for subjects_item_data in self.subjects:
                subjects_item = subjects_item_data.to_dict()

                subjects.append(subjects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if default_role is not UNSET:
            field_dict["default_role"] = default_role
        if subjects is not UNSET:
            field_dict["subjects"] = subjects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.team_subject import TeamSubject

        d = src_dict.copy()
        name = d.pop("name")

        default_role = d.pop("default_role", UNSET)

        subjects = []
        _subjects = d.pop("subjects", UNSET)
        for subjects_item_data in _subjects or []:
            subjects_item = TeamSubject.from_dict(subjects_item_data)

            subjects.append(subjects_item)

        team = cls(
            name=name,
            default_role=default_role,
            subjects=subjects,
        )

        team.additional_properties = d
        return team

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
