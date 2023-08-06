from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FormViewFieldOptionsCondition")


@attr.s(auto_attribs=True)
class FormViewFieldOptionsCondition:
    """
    Attributes:
        id (int):
        field (int):
        type (str): Indicates how the field's value must be compared to the filter's value. The filter is always in this
            order `field` `type` `value` (example: `field_1` `contains` `Test`).
        value (Union[Unset, str]): The filter value that must be compared to the field's value.
    """

    id: int
    field: int
    type: str
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        field = self.field
        type = self.type
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "field": field,
                "type": type,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        field = d.pop("field")

        type = d.pop("type")

        value = d.pop("value", UNSET)

        form_view_field_options_condition = cls(
            id=id,
            field=field,
            type=type,
            value=value,
        )

        form_view_field_options_condition.additional_properties = d
        return form_view_field_options_condition

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
