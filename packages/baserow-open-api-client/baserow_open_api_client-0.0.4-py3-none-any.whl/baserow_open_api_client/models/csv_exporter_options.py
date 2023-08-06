from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.csv_column_separator_enum import CsvColumnSeparatorEnum
from ..models.export_charset_enum import ExportCharsetEnum
from ..models.exporter_type_enum import ExporterTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CsvExporterOptions")


@attr.s(auto_attribs=True)
class CsvExporterOptions:
    """
    Attributes:
        exporter_type (ExporterTypeEnum):
        view_id (Union[Unset, None, int]): Optional: The view for this table to export using its filters, sorts and
            other view specific settings.
        export_charset (Union[Unset, ExportCharsetEnum]):  Default: ExportCharsetEnum.UTF_8.
        csv_column_separator (Union[Unset, CsvColumnSeparatorEnum]):  Default: CsvColumnSeparatorEnum.VALUE_0.
        csv_include_header (Union[Unset, bool]): Whether or not to generate a header row at the top of the csv file.
            Default: True.
    """

    exporter_type: ExporterTypeEnum
    view_id: Union[Unset, None, int] = UNSET
    export_charset: Union[Unset, ExportCharsetEnum] = ExportCharsetEnum.UTF_8
    csv_column_separator: Union[Unset, CsvColumnSeparatorEnum] = CsvColumnSeparatorEnum.VALUE_0
    csv_include_header: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        exporter_type = self.exporter_type.value

        view_id = self.view_id
        export_charset: Union[Unset, str] = UNSET
        if not isinstance(self.export_charset, Unset):
            export_charset = self.export_charset.value

        csv_column_separator: Union[Unset, str] = UNSET
        if not isinstance(self.csv_column_separator, Unset):
            csv_column_separator = self.csv_column_separator.value

        csv_include_header = self.csv_include_header

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exporter_type": exporter_type,
            }
        )
        if view_id is not UNSET:
            field_dict["view_id"] = view_id
        if export_charset is not UNSET:
            field_dict["export_charset"] = export_charset
        if csv_column_separator is not UNSET:
            field_dict["csv_column_separator"] = csv_column_separator
        if csv_include_header is not UNSET:
            field_dict["csv_include_header"] = csv_include_header

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exporter_type = ExporterTypeEnum(d.pop("exporter_type"))

        view_id = d.pop("view_id", UNSET)

        _export_charset = d.pop("export_charset", UNSET)
        export_charset: Union[Unset, ExportCharsetEnum]
        if isinstance(_export_charset, Unset):
            export_charset = UNSET
        else:
            export_charset = ExportCharsetEnum(_export_charset)

        _csv_column_separator = d.pop("csv_column_separator", UNSET)
        csv_column_separator: Union[Unset, CsvColumnSeparatorEnum]
        if isinstance(_csv_column_separator, Unset):
            csv_column_separator = UNSET
        else:
            csv_column_separator = CsvColumnSeparatorEnum(_csv_column_separator)

        csv_include_header = d.pop("csv_include_header", UNSET)

        csv_exporter_options = cls(
            exporter_type=exporter_type,
            view_id=view_id,
            export_charset=export_charset,
            csv_column_separator=csv_column_separator,
            csv_include_header=csv_include_header,
        )

        csv_exporter_options.additional_properties = d
        return csv_exporter_options

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
