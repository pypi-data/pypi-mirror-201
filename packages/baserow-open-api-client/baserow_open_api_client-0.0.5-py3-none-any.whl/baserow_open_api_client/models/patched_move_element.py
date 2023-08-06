from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedMoveElement")


@attr.s(auto_attribs=True)
class PatchedMoveElement:
    """
    Attributes:
        before_id (Union[Unset, None, int]): If provided, the element is moved before the element with this Id.
            Otherwise the element is placed at the end of the page.
    """

    before_id: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        before_id = self.before_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if before_id is not UNSET:
            field_dict["before_id"] = before_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        before_id = d.pop("before_id", UNSET)

        patched_move_element = cls(
            before_id=before_id,
        )

        patched_move_element.additional_properties = d
        return patched_move_element

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
