from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkspaceUserEnterpriseTeam")


@attr.s(auto_attribs=True)
class WorkspaceUserEnterpriseTeam:
    """A serializer for the `WorkspaceUserSerializer.teams` field.

    Attributes:
        id (int): The unique identifier for this team.
        name (str): The team name that this group user belongs to.
    """

    id: int
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        workspace_user_enterprise_team = cls(
            id=id,
            name=name,
        )

        workspace_user_enterprise_team.additional_properties = d
        return workspace_user_enterprise_team

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
