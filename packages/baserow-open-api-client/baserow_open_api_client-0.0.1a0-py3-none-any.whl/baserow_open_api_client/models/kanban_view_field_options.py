from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="KanbanViewFieldOptions")


@attr.s(auto_attribs=True)
class KanbanViewFieldOptions:
    """
    Attributes:
        hidden (Union[Unset, bool]): Whether or not the field should be hidden in the card.
        order (Union[Unset, int]): The order that the field has in the view. Lower value is first.
    """

    hidden: Union[Unset, bool] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hidden = self.hidden
        order = self.order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hidden = d.pop("hidden", UNSET)

        order = d.pop("order", UNSET)

        kanban_view_field_options = cls(
            hidden=hidden,
            order=order,
        )

        kanban_view_field_options.additional_properties = d
        return kanban_view_field_options

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
