from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RowMetadata")


@attr.s(auto_attribs=True)
class RowMetadata:
    """
    Attributes:
        row_comment_count (Union[Unset, int]): How many row comments exist for this row.
    """

    row_comment_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_comment_count = self.row_comment_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if row_comment_count is not UNSET:
            field_dict["row_comment_count"] = row_comment_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        row_comment_count = d.pop("row_comment_count", UNSET)

        row_metadata = cls(
            row_comment_count=row_comment_count,
        )

        row_metadata.additional_properties = d
        return row_metadata

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
