from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="SelectColorValueProviderConf")


@attr.s(auto_attribs=True)
class SelectColorValueProviderConf:
    """
    Attributes:
        field_id (Optional[int]): An id of a select field of the table. The value provider return the color of the
            selected option for each row.
    """

    field_id: Optional[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_id = self.field_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field_id": field_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_id = d.pop("field_id")

        select_color_value_provider_conf = cls(
            field_id=field_id,
        )

        select_color_value_provider_conf.additional_properties = d
        return select_color_value_provider_conf

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
