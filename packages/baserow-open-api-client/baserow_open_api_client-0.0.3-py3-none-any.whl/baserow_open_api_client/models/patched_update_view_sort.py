from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.order_enum import OrderEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUpdateViewSort")


@attr.s(auto_attribs=True)
class PatchedUpdateViewSort:
    """
    Attributes:
        field (Union[Unset, int]): The field that must be sorted on.
        order (Union[Unset, OrderEnum]):
    """

    field: Union[Unset, int] = UNSET
    order: Union[Unset, OrderEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field = self.field
        order: Union[Unset, str] = UNSET
        if not isinstance(self.order, Unset):
            order = self.order.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field", UNSET)

        _order = d.pop("order", UNSET)
        order: Union[Unset, OrderEnum]
        if isinstance(_order, Unset):
            order = UNSET
        else:
            order = OrderEnum(_order)

        patched_update_view_sort = cls(
            field=field,
            order=order,
        )

        patched_update_view_sort.additional_properties = d
        return patched_update_view_sort

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
