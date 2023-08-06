from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.trash_structure_group import TrashStructureGroup


T = TypeVar("T", bound="TrashStructure")


@attr.s(auto_attribs=True)
class TrashStructure:
    """
    Attributes:
        groups (List['TrashStructureGroup']): An array of group trash structure records. Deprecated, please use
            `workspaces`.
        workspaces (List['TrashStructureGroup']): An array of workspace trash structure records
    """

    groups: List["TrashStructureGroup"]
    workspaces: List["TrashStructureGroup"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()

            groups.append(groups_item)

        workspaces = []
        for workspaces_item_data in self.workspaces:
            workspaces_item = workspaces_item_data.to_dict()

            workspaces.append(workspaces_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groups": groups,
                "workspaces": workspaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trash_structure_group import TrashStructureGroup

        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = TrashStructureGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        workspaces = []
        _workspaces = d.pop("workspaces")
        for workspaces_item_data in _workspaces:
            workspaces_item = TrashStructureGroup.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        trash_structure = cls(
            groups=groups,
            workspaces=workspaces,
        )

        trash_structure.additional_properties = d
        return trash_structure

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
