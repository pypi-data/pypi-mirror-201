from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.array_formula_type_enum import ArrayFormulaTypeEnum
from ..models.date_format_enum import DateFormatEnum
from ..models.date_time_format_enum import DateTimeFormatEnum
from ..models.formula_type_enum import FormulaTypeEnum
from ..models.number_decimal_places_enum import NumberDecimalPlacesEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormulaFieldField")


@attr.s(auto_attribs=True)
class FormulaFieldField:
    """
    Attributes:
        id (int):
        table_id (int):
        name (str):
        order (int): Lowest first.
        type (str): The type of the related field.
        read_only (bool): Indicates whether the field is a read only field. If true, it's not possible to update the
            cell value.
        error (str):
        nullable (bool):
        formula (str):
        primary (Union[Unset, bool]): Indicates if the field is a primary field. If `true` the field cannot be deleted
            and the value should represent the whole row.
        date_format (Union[DateFormatEnum, None, Unset]): EU (20/02/2020), US (02/20/2020) or ISO (2020-02-20)
        date_time_format (Union[DateTimeFormatEnum, None, Unset]): 24 (14:30) or 12 (02:30 PM)
        number_decimal_places (Union[None, NumberDecimalPlacesEnum, Unset]): The amount of digits allowed after the
            point.
        array_formula_type (Union[ArrayFormulaTypeEnum, None, Unset]):
        date_include_time (Union[Unset, None, bool]): Indicates if the field also includes a time.
        date_force_timezone (Union[Unset, None, str]): Force a timezone for the field overriding user profile settings.
        date_show_tzinfo (Union[Unset, None, bool]): Indicates if the time zone should be shown.
        formula_type (Union[Unset, FormulaTypeEnum]):
    """

    id: int
    table_id: int
    name: str
    order: int
    type: str
    read_only: bool
    error: str
    nullable: bool
    formula: str
    primary: Union[Unset, bool] = UNSET
    date_format: Union[DateFormatEnum, None, Unset] = UNSET
    date_time_format: Union[DateTimeFormatEnum, None, Unset] = UNSET
    number_decimal_places: Union[None, NumberDecimalPlacesEnum, Unset] = UNSET
    array_formula_type: Union[ArrayFormulaTypeEnum, None, Unset] = UNSET
    date_include_time: Union[Unset, None, bool] = UNSET
    date_force_timezone: Union[Unset, None, str] = UNSET
    date_show_tzinfo: Union[Unset, None, bool] = UNSET
    formula_type: Union[Unset, FormulaTypeEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        name = self.name
        order = self.order
        type = self.type
        read_only = self.read_only
        error = self.error
        nullable = self.nullable
        formula = self.formula
        primary = self.primary
        date_format: Union[None, Unset, str]
        if isinstance(self.date_format, Unset):
            date_format = UNSET
        elif self.date_format is None:
            date_format = None

        elif isinstance(self.date_format, DateFormatEnum):
            date_format = UNSET
            if not isinstance(self.date_format, Unset):
                date_format = self.date_format.value

        else:
            date_format = self.date_format

        date_time_format: Union[None, Unset, str]
        if isinstance(self.date_time_format, Unset):
            date_time_format = UNSET
        elif self.date_time_format is None:
            date_time_format = None

        elif isinstance(self.date_time_format, DateTimeFormatEnum):
            date_time_format = UNSET
            if not isinstance(self.date_time_format, Unset):
                date_time_format = self.date_time_format.value

        else:
            date_time_format = self.date_time_format

        number_decimal_places: Union[None, Unset, int]
        if isinstance(self.number_decimal_places, Unset):
            number_decimal_places = UNSET
        elif self.number_decimal_places is None:
            number_decimal_places = None

        elif isinstance(self.number_decimal_places, NumberDecimalPlacesEnum):
            number_decimal_places = UNSET
            if not isinstance(self.number_decimal_places, Unset):
                number_decimal_places = self.number_decimal_places.value

        else:
            number_decimal_places = self.number_decimal_places

        array_formula_type: Union[None, Unset, str]
        if isinstance(self.array_formula_type, Unset):
            array_formula_type = UNSET
        elif self.array_formula_type is None:
            array_formula_type = None

        elif isinstance(self.array_formula_type, ArrayFormulaTypeEnum):
            array_formula_type = UNSET
            if not isinstance(self.array_formula_type, Unset):
                array_formula_type = self.array_formula_type.value

        else:
            array_formula_type = self.array_formula_type

        date_include_time = self.date_include_time
        date_force_timezone = self.date_force_timezone
        date_show_tzinfo = self.date_show_tzinfo
        formula_type: Union[Unset, str] = UNSET
        if not isinstance(self.formula_type, Unset):
            formula_type = self.formula_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "name": name,
                "order": order,
                "type": type,
                "read_only": read_only,
                "error": error,
                "nullable": nullable,
                "formula": formula,
            }
        )
        if primary is not UNSET:
            field_dict["primary"] = primary
        if date_format is not UNSET:
            field_dict["date_format"] = date_format
        if date_time_format is not UNSET:
            field_dict["date_time_format"] = date_time_format
        if number_decimal_places is not UNSET:
            field_dict["number_decimal_places"] = number_decimal_places
        if array_formula_type is not UNSET:
            field_dict["array_formula_type"] = array_formula_type
        if date_include_time is not UNSET:
            field_dict["date_include_time"] = date_include_time
        if date_force_timezone is not UNSET:
            field_dict["date_force_timezone"] = date_force_timezone
        if date_show_tzinfo is not UNSET:
            field_dict["date_show_tzinfo"] = date_show_tzinfo
        if formula_type is not UNSET:
            field_dict["formula_type"] = formula_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        read_only = d.pop("read_only")

        error = d.pop("error")

        nullable = d.pop("nullable")

        formula = d.pop("formula")

        primary = d.pop("primary", UNSET)

        def _parse_date_format(data: object) -> Union[DateFormatEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _date_format_type_0 = data
                date_format_type_0: Union[Unset, DateFormatEnum]
                if isinstance(_date_format_type_0, Unset):
                    date_format_type_0 = UNSET
                else:
                    date_format_type_0 = DateFormatEnum(_date_format_type_0)

                return date_format_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DateFormatEnum, None, Unset], data)

        date_format = _parse_date_format(d.pop("date_format", UNSET))

        def _parse_date_time_format(data: object) -> Union[DateTimeFormatEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _date_time_format_type_0 = data
                date_time_format_type_0: Union[Unset, DateTimeFormatEnum]
                if isinstance(_date_time_format_type_0, Unset):
                    date_time_format_type_0 = UNSET
                else:
                    date_time_format_type_0 = DateTimeFormatEnum(_date_time_format_type_0)

                return date_time_format_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DateTimeFormatEnum, None, Unset], data)

        date_time_format = _parse_date_time_format(d.pop("date_time_format", UNSET))

        def _parse_number_decimal_places(data: object) -> Union[None, NumberDecimalPlacesEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                _number_decimal_places_type_0 = data
                number_decimal_places_type_0: Union[Unset, NumberDecimalPlacesEnum]
                if isinstance(_number_decimal_places_type_0, Unset):
                    number_decimal_places_type_0 = UNSET
                else:
                    number_decimal_places_type_0 = NumberDecimalPlacesEnum(_number_decimal_places_type_0)

                return number_decimal_places_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, NumberDecimalPlacesEnum, Unset], data)

        number_decimal_places = _parse_number_decimal_places(d.pop("number_decimal_places", UNSET))

        def _parse_array_formula_type(data: object) -> Union[ArrayFormulaTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _array_formula_type_type_0 = data
                array_formula_type_type_0: Union[Unset, ArrayFormulaTypeEnum]
                if isinstance(_array_formula_type_type_0, Unset):
                    array_formula_type_type_0 = UNSET
                else:
                    array_formula_type_type_0 = ArrayFormulaTypeEnum(_array_formula_type_type_0)

                return array_formula_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ArrayFormulaTypeEnum, None, Unset], data)

        array_formula_type = _parse_array_formula_type(d.pop("array_formula_type", UNSET))

        date_include_time = d.pop("date_include_time", UNSET)

        date_force_timezone = d.pop("date_force_timezone", UNSET)

        date_show_tzinfo = d.pop("date_show_tzinfo", UNSET)

        _formula_type = d.pop("formula_type", UNSET)
        formula_type: Union[Unset, FormulaTypeEnum]
        if isinstance(_formula_type, Unset):
            formula_type = UNSET
        else:
            formula_type = FormulaTypeEnum(_formula_type)

        formula_field_field = cls(
            id=id,
            table_id=table_id,
            name=name,
            order=order,
            type=type,
            read_only=read_only,
            error=error,
            nullable=nullable,
            formula=formula,
            primary=primary,
            date_format=date_format,
            date_time_format=date_time_format,
            number_decimal_places=number_decimal_places,
            array_formula_type=array_formula_type,
            date_include_time=date_include_time,
            date_force_timezone=date_force_timezone,
            date_show_tzinfo=date_show_tzinfo,
            formula_type=formula_type,
        )

        formula_field_field.additional_properties = d
        return formula_field_field

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
