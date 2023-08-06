from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..models.type_9_cb_enum import Type9CbEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConditionalColorValueProviderConfColorFilter")


@attr.s(auto_attribs=True)
class ConditionalColorValueProviderConfColorFilter:
    """
    Attributes:
        id (str): A unique identifier for this condition.
        field (Optional[int]): The field of which the value must be compared to the filter value.
        type (Union[None, Type9CbEnum]): Indicates how the field's value must be compared to the filter's value. The
            filter is always in this order `field` `type` `value` (example: `field_1` `contains` `Test`).
        value (Union[Unset, str]): The field of which the value must be compared to the filter value. Default: ''.
    """

    id: str
    field: Optional[int]
    type: Union[None, Type9CbEnum]
    value: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        field = self.field
        type: Union[None, str]
        if self.type is None:
            type = None

        elif isinstance(self.type, Type9CbEnum):
            type = self.type.value

        else:
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

        def _parse_type(data: object) -> Union[None, Type9CbEnum]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = Type9CbEnum(data)

                return type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Type9CbEnum], data)

        type = _parse_type(d.pop("type"))

        value = d.pop("value", UNSET)

        conditional_color_value_provider_conf_color_filter = cls(
            id=id,
            field=field,
            type=type,
            value=value,
        )

        conditional_color_value_provider_conf_color_filter.additional_properties = d
        return conditional_color_value_provider_conf_color_filter

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
