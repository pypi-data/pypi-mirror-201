from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.kanban_view_example_response_stack import KanbanViewExampleResponseStack
    from ..models.kanban_view_field_options import KanbanViewFieldOptions


T = TypeVar("T", bound="KanbanViewExampleResponse")


@attr.s(auto_attribs=True)
class KanbanViewExampleResponse:
    """
    Attributes:
        option_id (KanbanViewExampleResponseStack):
        field_options (List['KanbanViewFieldOptions']):
    """

    option_id: "KanbanViewExampleResponseStack"
    field_options: List["KanbanViewFieldOptions"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        option_id = self.option_id.to_dict()

        field_options = []
        for field_options_item_data in self.field_options:
            field_options_item = field_options_item_data.to_dict()

            field_options.append(field_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "OPTION_ID": option_id,
                "field_options": field_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.kanban_view_example_response_stack import KanbanViewExampleResponseStack
        from ..models.kanban_view_field_options import KanbanViewFieldOptions

        d = src_dict.copy()
        option_id = KanbanViewExampleResponseStack.from_dict(d.pop("OPTION_ID"))

        field_options = []
        _field_options = d.pop("field_options")
        for field_options_item_data in _field_options:
            field_options_item = KanbanViewFieldOptions.from_dict(field_options_item_data)

            field_options.append(field_options_item)

        kanban_view_example_response = cls(
            option_id=option_id,
            field_options=field_options,
        )

        kanban_view_example_response.additional_properties = d
        return kanban_view_example_response

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
