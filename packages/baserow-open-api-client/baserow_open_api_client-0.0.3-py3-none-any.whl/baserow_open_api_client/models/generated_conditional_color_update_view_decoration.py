from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.blank_enum import BlankEnum
from ..models.type_fc_4_enum import TypeFc4Enum
from ..models.value_provider_type_enum import ValueProviderTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.conditional_color_value_provider_conf_colors import ConditionalColorValueProviderConfColors


T = TypeVar("T", bound="GeneratedConditionalColorUpdateViewDecoration")


@attr.s(auto_attribs=True)
class GeneratedConditionalColorUpdateViewDecoration:
    """
    Attributes:
        type (Union[Unset, TypeFc4Enum]):
        value_provider_type (Union[BlankEnum, Unset, ValueProviderTypeEnum]): The value provider type that gives the
            value to the decorator.
        value_provider_conf (Union[Unset, ConditionalColorValueProviderConfColors]):
        order (Union[Unset, int]): The position of the decorator has within the view, lowest first. If there is another
            decorator with the same order value then the decorator with the lowest id must be shown first.
    """

    type: Union[Unset, TypeFc4Enum] = UNSET
    value_provider_type: Union[BlankEnum, Unset, ValueProviderTypeEnum] = UNSET
    value_provider_conf: Union[Unset, "ConditionalColorValueProviderConfColors"] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value_provider_type: Union[Unset, str]
        if isinstance(self.value_provider_type, Unset):
            value_provider_type = UNSET

        elif isinstance(self.value_provider_type, ValueProviderTypeEnum):
            value_provider_type = UNSET
            if not isinstance(self.value_provider_type, Unset):
                value_provider_type = self.value_provider_type.value

        else:
            value_provider_type = UNSET
            if not isinstance(self.value_provider_type, Unset):
                value_provider_type = self.value_provider_type.value

        value_provider_conf: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value_provider_conf, Unset):
            value_provider_conf = self.value_provider_conf.to_dict()

        order = self.order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value_provider_type is not UNSET:
            field_dict["value_provider_type"] = value_provider_type
        if value_provider_conf is not UNSET:
            field_dict["value_provider_conf"] = value_provider_conf
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.conditional_color_value_provider_conf_colors import ConditionalColorValueProviderConfColors

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, TypeFc4Enum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TypeFc4Enum(_type)

        def _parse_value_provider_type(data: object) -> Union[BlankEnum, Unset, ValueProviderTypeEnum]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _value_provider_type_type_0 = data
                value_provider_type_type_0: Union[Unset, ValueProviderTypeEnum]
                if isinstance(_value_provider_type_type_0, Unset):
                    value_provider_type_type_0 = UNSET
                else:
                    value_provider_type_type_0 = ValueProviderTypeEnum(_value_provider_type_type_0)

                return value_provider_type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            _value_provider_type_type_1 = data
            value_provider_type_type_1: Union[Unset, BlankEnum]
            if isinstance(_value_provider_type_type_1, Unset):
                value_provider_type_type_1 = UNSET
            else:
                value_provider_type_type_1 = BlankEnum(_value_provider_type_type_1)

            return value_provider_type_type_1

        value_provider_type = _parse_value_provider_type(d.pop("value_provider_type", UNSET))

        _value_provider_conf = d.pop("value_provider_conf", UNSET)
        value_provider_conf: Union[Unset, ConditionalColorValueProviderConfColors]
        if isinstance(_value_provider_conf, Unset):
            value_provider_conf = UNSET
        else:
            value_provider_conf = ConditionalColorValueProviderConfColors.from_dict(_value_provider_conf)

        order = d.pop("order", UNSET)

        generated_conditional_color_update_view_decoration = cls(
            type=type,
            value_provider_type=value_provider_type,
            value_provider_conf=value_provider_conf,
            order=order,
        )

        generated_conditional_color_update_view_decoration.additional_properties = d
        return generated_conditional_color_update_view_decoration

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
