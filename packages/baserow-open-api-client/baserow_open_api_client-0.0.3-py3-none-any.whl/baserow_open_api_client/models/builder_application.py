from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.page import Page
    from ..models.workspace import Workspace


T = TypeVar("T", bound="BuilderApplication")


@attr.s(auto_attribs=True)
class BuilderApplication:
    """
    Attributes:
        id (int):
        name (str):
        order (int):
        type (str):
        group (Workspace):
        workspace (Workspace):
        pages (List['Page']): This field is specific to the `builder` application and contains an array of pages that
            are in the builder.
    """

    id: int
    name: str
    order: int
    type: str
    group: "Workspace"
    workspace: "Workspace"
    pages: List["Page"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        order = self.order
        type = self.type
        group = self.group.to_dict()

        workspace = self.workspace.to_dict()

        pages = []
        for pages_item_data in self.pages:
            pages_item = pages_item_data.to_dict()

            pages.append(pages_item)

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
                "pages": pages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page import Page
        from ..models.workspace import Workspace

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        group = Workspace.from_dict(d.pop("group"))

        workspace = Workspace.from_dict(d.pop("workspace"))

        pages = []
        _pages = d.pop("pages")
        for pages_item_data in _pages:
            pages_item = Page.from_dict(pages_item_data)

            pages.append(pages_item)

        builder_application = cls(
            id=id,
            name=name,
            order=order,
            type=type,
            group=group,
            workspace=workspace,
            pages=pages,
        )

        builder_application.additional_properties = d
        return builder_application

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
