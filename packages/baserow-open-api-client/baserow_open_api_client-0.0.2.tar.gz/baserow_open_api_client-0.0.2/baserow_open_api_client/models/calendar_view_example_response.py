from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.calendar_view_example_response_stack import CalendarViewExampleResponseStack
    from ..models.calendar_view_field_options import CalendarViewFieldOptions


T = TypeVar("T", bound="CalendarViewExampleResponse")


@attr.s(auto_attribs=True)
class CalendarViewExampleResponse:
    """
    Attributes:
        date (CalendarViewExampleResponseStack):
        field_options (List['CalendarViewFieldOptions']):
    """

    date: "CalendarViewExampleResponseStack"
    field_options: List["CalendarViewFieldOptions"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date = self.date.to_dict()

        field_options = []
        for field_options_item_data in self.field_options:
            field_options_item = field_options_item_data.to_dict()

            field_options.append(field_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "DATE": date,
                "field_options": field_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.calendar_view_example_response_stack import CalendarViewExampleResponseStack
        from ..models.calendar_view_field_options import CalendarViewFieldOptions

        d = src_dict.copy()
        date = CalendarViewExampleResponseStack.from_dict(d.pop("DATE"))

        field_options = []
        _field_options = d.pop("field_options")
        for field_options_item_data in _field_options:
            field_options_item = CalendarViewFieldOptions.from_dict(field_options_item_data)

            field_options.append(field_options_item)

        calendar_view_example_response = cls(
            date=date,
            field_options=field_options,
        )

        calendar_view_example_response.additional_properties = d
        return calendar_view_example_response

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
