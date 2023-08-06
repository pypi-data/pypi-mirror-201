from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.date_format_enum import DateFormatEnum
from ..models.date_time_format_enum import DateTimeFormatEnum
from ..models.type_77b_enum import Type77BEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestCreatedOnFieldUpdateField")


@attr.s(auto_attribs=True)
class RequestCreatedOnFieldUpdateField:
    """
    Attributes:
        name (Union[Unset, str]):
        type (Union[Unset, Type77BEnum]):
        date_format (Union[Unset, DateFormatEnum]):
        date_include_time (Union[Unset, bool]): Indicates if the field also includes a time.
        date_time_format (Union[Unset, DateTimeFormatEnum]):
        date_show_tzinfo (Union[Unset, bool]): Indicates if the timezone should be shown.
        date_force_timezone (Union[Unset, None, str]): Force a timezone for the field overriding user profile settings.
        date_force_timezone_offset (Union[Unset, None, int]): ('A UTC offset in minutes to add to all the field
            datetimes values.',)
    """

    name: Union[Unset, str] = UNSET
    type: Union[Unset, Type77BEnum] = UNSET
    date_format: Union[Unset, DateFormatEnum] = UNSET
    date_include_time: Union[Unset, bool] = UNSET
    date_time_format: Union[Unset, DateTimeFormatEnum] = UNSET
    date_show_tzinfo: Union[Unset, bool] = UNSET
    date_force_timezone: Union[Unset, None, str] = UNSET
    date_force_timezone_offset: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        date_format: Union[Unset, str] = UNSET
        if not isinstance(self.date_format, Unset):
            date_format = self.date_format.value

        date_include_time = self.date_include_time
        date_time_format: Union[Unset, str] = UNSET
        if not isinstance(self.date_time_format, Unset):
            date_time_format = self.date_time_format.value

        date_show_tzinfo = self.date_show_tzinfo
        date_force_timezone = self.date_force_timezone
        date_force_timezone_offset = self.date_force_timezone_offset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if date_format is not UNSET:
            field_dict["date_format"] = date_format
        if date_include_time is not UNSET:
            field_dict["date_include_time"] = date_include_time
        if date_time_format is not UNSET:
            field_dict["date_time_format"] = date_time_format
        if date_show_tzinfo is not UNSET:
            field_dict["date_show_tzinfo"] = date_show_tzinfo
        if date_force_timezone is not UNSET:
            field_dict["date_force_timezone"] = date_force_timezone
        if date_force_timezone_offset is not UNSET:
            field_dict["date_force_timezone_offset"] = date_force_timezone_offset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, Type77BEnum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = Type77BEnum(_type)

        _date_format = d.pop("date_format", UNSET)
        date_format: Union[Unset, DateFormatEnum]
        if isinstance(_date_format, Unset):
            date_format = UNSET
        else:
            date_format = DateFormatEnum(_date_format)

        date_include_time = d.pop("date_include_time", UNSET)

        _date_time_format = d.pop("date_time_format", UNSET)
        date_time_format: Union[Unset, DateTimeFormatEnum]
        if isinstance(_date_time_format, Unset):
            date_time_format = UNSET
        else:
            date_time_format = DateTimeFormatEnum(_date_time_format)

        date_show_tzinfo = d.pop("date_show_tzinfo", UNSET)

        date_force_timezone = d.pop("date_force_timezone", UNSET)

        date_force_timezone_offset = d.pop("date_force_timezone_offset", UNSET)

        request_created_on_field_update_field = cls(
            name=name,
            type=type,
            date_format=date_format,
            date_include_time=date_include_time,
            date_time_format=date_time_format,
            date_show_tzinfo=date_show_tzinfo,
            date_force_timezone=date_force_timezone,
            date_force_timezone_offset=date_force_timezone_offset,
        )

        request_created_on_field_update_field.additional_properties = d
        return request_created_on_field_update_field

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
