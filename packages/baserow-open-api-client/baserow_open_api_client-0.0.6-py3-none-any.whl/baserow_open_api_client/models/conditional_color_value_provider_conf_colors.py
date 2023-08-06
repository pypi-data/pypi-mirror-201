from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.conditional_color_value_provider_conf_color import ConditionalColorValueProviderConfColor


T = TypeVar("T", bound="ConditionalColorValueProviderConfColors")


@attr.s(auto_attribs=True)
class ConditionalColorValueProviderConfColors:
    """
    Attributes:
        colors (List['ConditionalColorValueProviderConfColor']): A list of color items. For each row, the value provider
            try to match the defined colors one by one in the given order. The first matching color is returned to the
            decorator.
    """

    colors: List["ConditionalColorValueProviderConfColor"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        colors = []
        for colors_item_data in self.colors:
            colors_item = colors_item_data.to_dict()

            colors.append(colors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "colors": colors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conditional_color_value_provider_conf_color import ConditionalColorValueProviderConfColor

        d = src_dict.copy()
        colors = []
        _colors = d.pop("colors")
        for colors_item_data in _colors:
            colors_item = ConditionalColorValueProviderConfColor.from_dict(colors_item_data)

            colors.append(colors_item)

        conditional_color_value_provider_conf_colors = cls(
            colors=colors,
        )

        conditional_color_value_provider_conf_colors.additional_properties = d
        return conditional_color_value_provider_conf_colors

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
