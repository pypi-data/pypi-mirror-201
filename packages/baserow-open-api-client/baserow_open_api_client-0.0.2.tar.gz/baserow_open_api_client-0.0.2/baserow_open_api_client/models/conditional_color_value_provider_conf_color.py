from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conditional_color_value_provider_conf_color_filter import ConditionalColorValueProviderConfColorFilter


T = TypeVar("T", bound="ConditionalColorValueProviderConfColor")


@attr.s(auto_attribs=True)
class ConditionalColorValueProviderConfColor:
    """
    Attributes:
        id (str): A unique identifier for this condition.
        color (str): The color the decorator should take if the defined conditions apply.
        filters (List['ConditionalColorValueProviderConfColorFilter']): A list of conditions that the row must meet to
            get the selected color. This list of conditions can be empty, in that case, this color will always match the row
            values.
        operator (Union[Unset, ConditionTypeEnum]):  Default: ConditionTypeEnum.AND.
    """

    id: str
    color: str
    filters: List["ConditionalColorValueProviderConfColorFilter"]
    operator: Union[Unset, ConditionTypeEnum] = ConditionTypeEnum.AND
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        color = self.color
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "color": color,
                "filters": filters,
            }
        )
        if operator is not UNSET:
            field_dict["operator"] = operator

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conditional_color_value_provider_conf_color_filter import (
            ConditionalColorValueProviderConfColorFilter,
        )

        d = src_dict.copy()
        id = d.pop("id")

        color = d.pop("color")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = ConditionalColorValueProviderConfColorFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, ConditionTypeEnum]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = ConditionTypeEnum(_operator)

        conditional_color_value_provider_conf_color = cls(
            id=id,
            color=color,
            filters=filters,
            operator=operator,
        )

        conditional_color_value_provider_conf_color.additional_properties = d
        return conditional_color_value_provider_conf_color

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
