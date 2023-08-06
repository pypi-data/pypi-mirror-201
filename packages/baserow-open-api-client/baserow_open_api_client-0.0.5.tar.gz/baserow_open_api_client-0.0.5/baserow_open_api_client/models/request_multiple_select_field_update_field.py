from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.select_option import SelectOption


T = TypeVar("T", bound="RequestMultipleSelectFieldUpdateField")


@attr.s(auto_attribs=True)
class RequestMultipleSelectFieldUpdateField:
    """
    Attributes:
        name (Union[Unset, str]):
        type (Union[Unset, Type77BEnum]):
        select_options (Union[Unset, List['SelectOption']]):
    """

    name: Union[Unset, str] = UNSET
    type: Union[Unset, Type77BEnum] = UNSET
    select_options: Union[Unset, List["SelectOption"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        select_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.select_options, Unset):
            select_options = []
            for select_options_item_data in self.select_options:
                select_options_item = select_options_item_data.to_dict()

                select_options.append(select_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if select_options is not UNSET:
            field_dict["select_options"] = select_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.select_option import SelectOption

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, Type77BEnum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = Type77BEnum(_type)

        select_options = []
        _select_options = d.pop("select_options", UNSET)
        for select_options_item_data in _select_options or []:
            select_options_item = SelectOption.from_dict(select_options_item_data)

            select_options.append(select_options_item)

        request_multiple_select_field_update_field = cls(
            name=name,
            type=type,
            select_options=select_options,
        )

        request_multiple_select_field_update_field.additional_properties = d
        return request_multiple_select_field_update_field

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
