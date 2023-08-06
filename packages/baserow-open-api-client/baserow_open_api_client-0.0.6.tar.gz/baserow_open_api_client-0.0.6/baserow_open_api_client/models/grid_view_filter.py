from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GridViewFilter")


@attr.s(auto_attribs=True)
class GridViewFilter:
    """
    Attributes:
        row_ids (List[int]): Only rows related to the provided ids are added to the response.
        field_ids (Union[Unset, List[int]]): Only the fields related to the provided ids are added to the response. If
            None are provided all fields will be returned.
    """

    row_ids: List[int]
    field_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_ids = self.row_ids

        field_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.field_ids, Unset):
            field_ids = self.field_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "row_ids": row_ids,
            }
        )
        if field_ids is not UNSET:
            field_dict["field_ids"] = field_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        row_ids = cast(List[int], d.pop("row_ids"))

        field_ids = cast(List[int], d.pop("field_ids", UNSET))

        grid_view_filter = cls(
            row_ids=row_ids,
            field_ids=field_ids,
        )

        grid_view_filter.additional_properties = d
        return grid_view_filter

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
