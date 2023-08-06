from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.workspace import Workspace


T = TypeVar("T", bound="SpecificApplication")


@attr.s(auto_attribs=True)
class SpecificApplication:
    """
    Attributes:
        id (int):
        name (str):
        order (int):
        type (str):
        group (Workspace):
        workspace (Workspace):
    """

    id: int
    name: str
    order: int
    type: str
    group: "Workspace"
    workspace: "Workspace"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        order = self.order
        type = self.type
        group = self.group.to_dict()

        workspace = self.workspace.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "order": order,
                "type": type,
                "group": group,
                "workspace": workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace import Workspace

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        group = Workspace.from_dict(d.pop("group"))

        workspace = Workspace.from_dict(d.pop("workspace"))

        specific_application = cls(
            id=id,
            name=name,
            order=order,
            type=type,
            group=group,
            workspace=workspace,
        )

        specific_application.additional_properties = d
        return specific_application

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
