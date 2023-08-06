from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..models.ownership_type_enum import OwnershipTypeEnum
from ..models.view_types_enum import ViewTypesEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CalendarViewCreateView")


@attr.s(auto_attribs=True)
class CalendarViewCreateView:
    """
    Attributes:
        name (str):
        type (ViewTypesEnum):
        ownership_type (Union[Unset, OwnershipTypeEnum]):  Default: OwnershipTypeEnum.COLLABORATIVE.
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
        date_field (Union[Unset, None, int]):
    """

    name: str
    type: ViewTypesEnum
    ownership_type: Union[Unset, OwnershipTypeEnum] = OwnershipTypeEnum.COLLABORATIVE
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
    date_field: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        ownership_type: Union[Unset, str] = UNSET
        if not isinstance(self.ownership_type, Unset):
            ownership_type = self.ownership_type.value

        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters_disabled = self.filters_disabled
        date_field = self.date_field

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if ownership_type is not UNSET:
            field_dict["ownership_type"] = ownership_type
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
        if date_field is not UNSET:
            field_dict["date_field"] = date_field

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = ViewTypesEnum(d.pop("type"))

        _ownership_type = d.pop("ownership_type", UNSET)
        ownership_type: Union[Unset, OwnershipTypeEnum]
        if isinstance(_ownership_type, Unset):
            ownership_type = UNSET
        else:
            ownership_type = OwnershipTypeEnum(_ownership_type)

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters_disabled = d.pop("filters_disabled", UNSET)

        date_field = d.pop("date_field", UNSET)

        calendar_view_create_view = cls(
            name=name,
            type=type,
            ownership_type=ownership_type,
            filter_type=filter_type,
            filters_disabled=filters_disabled,
            date_field=date_field,
        )

        calendar_view_create_view.additional_properties = d
        return calendar_view_create_view

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
