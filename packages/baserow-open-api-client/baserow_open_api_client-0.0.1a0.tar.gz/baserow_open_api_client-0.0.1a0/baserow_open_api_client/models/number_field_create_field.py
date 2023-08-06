from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.number_decimal_places_enum import NumberDecimalPlacesEnum
from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NumberFieldCreateField")


@attr.s(auto_attribs=True)
class NumberFieldCreateField:
    """
    Attributes:
        name (str):
        type (Type77BEnum):
        number_decimal_places (Union[Unset, NumberDecimalPlacesEnum]):
        number_negative (Union[Unset, bool]): Indicates if negative values are allowed.
    """

    name: str
    type: Type77BEnum
    number_decimal_places: Union[Unset, NumberDecimalPlacesEnum] = UNSET
    number_negative: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        number_decimal_places: Union[Unset, int] = UNSET
        if not isinstance(self.number_decimal_places, Unset):
            number_decimal_places = self.number_decimal_places.value

        number_negative = self.number_negative

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if number_decimal_places is not UNSET:
            field_dict["number_decimal_places"] = number_decimal_places
        if number_negative is not UNSET:
            field_dict["number_negative"] = number_negative

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = Type77BEnum(d.pop("type"))

        _number_decimal_places = d.pop("number_decimal_places", UNSET)
        number_decimal_places: Union[Unset, NumberDecimalPlacesEnum]
        if isinstance(_number_decimal_places, Unset):
            number_decimal_places = UNSET
        else:
            number_decimal_places = NumberDecimalPlacesEnum(_number_decimal_places)

        number_negative = d.pop("number_negative", UNSET)

        number_field_create_field = cls(
            name=name,
            type=type,
            number_decimal_places=number_decimal_places,
            number_negative=number_negative,
        )

        number_field_create_field.additional_properties = d
        return number_field_create_field

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
