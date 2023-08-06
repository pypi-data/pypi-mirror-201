from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.kanban_view_field_options import KanbanViewFieldOptions


T = TypeVar("T", bound="KanbanViewFieldOptionsWrapperFieldOptions")


@attr.s(auto_attribs=True)
class KanbanViewFieldOptionsWrapperFieldOptions:
    """An object containing the field id as key and the properties related to view as value."""

    additional_properties: Dict[str, "KanbanViewFieldOptions"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.kanban_view_field_options import KanbanViewFieldOptions

        d = src_dict.copy()
        kanban_view_field_options_wrapper_field_options = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = KanbanViewFieldOptions.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        kanban_view_field_options_wrapper_field_options.additional_properties = additional_properties
        return kanban_view_field_options_wrapper_field_options

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "KanbanViewFieldOptions":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "KanbanViewFieldOptions") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
