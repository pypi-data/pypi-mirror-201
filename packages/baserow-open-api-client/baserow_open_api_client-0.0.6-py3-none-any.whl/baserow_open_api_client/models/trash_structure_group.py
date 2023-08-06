from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.trash_structure_application import TrashStructureApplication


T = TypeVar("T", bound="TrashStructureGroup")


@attr.s(auto_attribs=True)
class TrashStructureGroup:
    """
    Attributes:
        id (int):
        trashed (bool):
        name (str):
        applications (List['TrashStructureApplication']):
    """

    id: int
    trashed: bool
    name: str
    applications: List["TrashStructureApplication"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        trashed = self.trashed
        name = self.name
        applications = []
        for applications_item_data in self.applications:
            applications_item = applications_item_data.to_dict()

            applications.append(applications_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "trashed": trashed,
                "name": name,
                "applications": applications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trash_structure_application import TrashStructureApplication

        d = src_dict.copy()
        id = d.pop("id")

        trashed = d.pop("trashed")

        name = d.pop("name")

        applications = []
        _applications = d.pop("applications")
        for applications_item_data in _applications:
            applications_item = TrashStructureApplication.from_dict(applications_item_data)

            applications.append(applications_item)

        trash_structure_group = cls(
            id=id,
            trashed=trashed,
            name=name,
            applications=applications,
        )

        trash_structure_group.additional_properties = d
        return trash_structure_group

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
