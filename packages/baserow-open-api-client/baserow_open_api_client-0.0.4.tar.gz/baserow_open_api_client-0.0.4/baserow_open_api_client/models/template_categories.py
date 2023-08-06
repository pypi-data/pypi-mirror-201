from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.template import Template


T = TypeVar("T", bound="TemplateCategories")


@attr.s(auto_attribs=True)
class TemplateCategories:
    """
    Attributes:
        id (int):
        name (str):
        templates (List['Template']):
    """

    id: int
    name: str
    templates: List["Template"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()

            templates.append(templates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "templates": templates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.template import Template

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        templates = []
        _templates = d.pop("templates")
        for templates_item_data in _templates:
            templates_item = Template.from_dict(templates_item_data)

            templates.append(templates_item)

        template_categories = cls(
            id=id,
            name=name,
            templates=templates,
        )

        template_categories.additional_properties = d
        return template_categories

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
