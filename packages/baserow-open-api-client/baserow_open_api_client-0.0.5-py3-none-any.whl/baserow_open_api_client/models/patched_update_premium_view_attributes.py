from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUpdatePremiumViewAttributes")


@attr.s(auto_attribs=True)
class PatchedUpdatePremiumViewAttributes:
    """
    Attributes:
        show_logo (Union[Unset, bool]):
    """

    show_logo: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        show_logo = self.show_logo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if show_logo is not UNSET:
            field_dict["show_logo"] = show_logo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        show_logo = d.pop("show_logo", UNSET)

        patched_update_premium_view_attributes = cls(
            show_logo=show_logo,
        )

        patched_update_premium_view_attributes.additional_properties = d
        return patched_update_premium_view_attributes

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
