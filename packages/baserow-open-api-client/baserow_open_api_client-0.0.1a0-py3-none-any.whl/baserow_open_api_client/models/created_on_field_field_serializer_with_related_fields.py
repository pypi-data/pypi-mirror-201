from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.date_format_enum import DateFormatEnum
from ..models.date_time_format_enum import DateTimeFormatEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field import Field


T = TypeVar("T", bound="CreatedOnFieldFieldSerializerWithRelatedFields")


@attr.s(auto_attribs=True)
class CreatedOnFieldFieldSerializerWithRelatedFields:
    """
    Attributes:
        id (int):
        table_id (int):
        order (int): Lowest first.
        type (str): The type of the related field.
        read_only (bool): Indicates whether the field is a read only field. If true, it's not possible to update the
            cell value.
        related_fields (List['Field']): A list of related fields which also changed.
        name (Union[Unset, str]):
        primary (Union[Unset, bool]): Indicates if the field is a primary field. If `true` the field cannot be deleted
            and the value should represent the whole row.
        date_format (Union[Unset, DateFormatEnum]):
        date_include_time (Union[Unset, bool]): Indicates if the field also includes a time.
        date_time_format (Union[Unset, DateTimeFormatEnum]):
        date_show_tzinfo (Union[Unset, bool]): Indicates if the timezone should be shown.
        date_force_timezone (Union[Unset, None, str]): Force a timezone for the field overriding user profile settings.
    """

    id: int
    table_id: int
    order: int
    type: str
    read_only: bool
    related_fields: List["Field"]
    name: Union[Unset, str] = UNSET
    primary: Union[Unset, bool] = UNSET
    date_format: Union[Unset, DateFormatEnum] = UNSET
    date_include_time: Union[Unset, bool] = UNSET
    date_time_format: Union[Unset, DateTimeFormatEnum] = UNSET
    date_show_tzinfo: Union[Unset, bool] = UNSET
    date_force_timezone: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        order = self.order
        type = self.type
        read_only = self.read_only
        related_fields = []
        for related_fields_item_data in self.related_fields:
            related_fields_item = related_fields_item_data.to_dict()

            related_fields.append(related_fields_item)

        name = self.name
        primary = self.primary
        date_format: Union[Unset, str] = UNSET
        if not isinstance(self.date_format, Unset):
            date_format = self.date_format.value

        date_include_time = self.date_include_time
        date_time_format: Union[Unset, str] = UNSET
        if not isinstance(self.date_time_format, Unset):
            date_time_format = self.date_time_format.value

        date_show_tzinfo = self.date_show_tzinfo
        date_force_timezone = self.date_force_timezone

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "order": order,
                "type": type,
                "read_only": read_only,
                "related_fields": related_fields,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if primary is not UNSET:
            field_dict["primary"] = primary
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field import Field

        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        order = d.pop("order")

        type = d.pop("type")

        read_only = d.pop("read_only")

        related_fields = []
        _related_fields = d.pop("related_fields")
        for related_fields_item_data in _related_fields:
            related_fields_item = Field.from_dict(related_fields_item_data)

            related_fields.append(related_fields_item)

        name = d.pop("name", UNSET)

        primary = d.pop("primary", UNSET)

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

        created_on_field_field_serializer_with_related_fields = cls(
            id=id,
            table_id=table_id,
            order=order,
            type=type,
            read_only=read_only,
            related_fields=related_fields,
            name=name,
            primary=primary,
            date_format=date_format,
            date_include_time=date_include_time,
            date_time_format=date_time_format,
            date_show_tzinfo=date_show_tzinfo,
            date_force_timezone=date_force_timezone,
        )

        created_on_field_field_serializer_with_related_fields.additional_properties = d
        return created_on_field_field_serializer_with_related_fields

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
