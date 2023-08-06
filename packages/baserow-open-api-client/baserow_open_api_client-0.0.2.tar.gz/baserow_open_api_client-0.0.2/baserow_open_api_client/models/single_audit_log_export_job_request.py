import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.csv_column_separator_enum import CsvColumnSeparatorEnum
from ..models.export_charset_enum import ExportCharsetEnum
from ..models.filter_action_type_enum import FilterActionTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SingleAuditLogExportJobRequest")


@attr.s(auto_attribs=True)
class SingleAuditLogExportJobRequest:
    """
    Attributes:
        created_on (datetime.datetime): The date and time when the export job was created.
        export_charset (Union[Unset, ExportCharsetEnum]):  Default: ExportCharsetEnum.UTF_8.
        csv_column_separator (Union[Unset, CsvColumnSeparatorEnum]):  Default: CsvColumnSeparatorEnum.VALUE_0.
        csv_first_row_header (Union[Unset, bool]): Whether or not to generate a header row at the top of the csv file.
            Default: True.
        filter_user_id (Union[Unset, int]): Optional: The user to filter the audit log by.
        filter_workspace_id (Union[Unset, int]): Optional: The workspace to filter the audit log by.
        filter_action_type (Union[Unset, FilterActionTypeEnum]):
        filter_from_timestamp (Union[Unset, datetime.datetime]): Optional: The start date to filter the audit log by.
        filter_to_timestamp (Union[Unset, datetime.datetime]): Optional: The end date to filter the audit log by.
    """

    created_on: datetime.datetime
    export_charset: Union[Unset, ExportCharsetEnum] = ExportCharsetEnum.UTF_8
    csv_column_separator: Union[Unset, CsvColumnSeparatorEnum] = CsvColumnSeparatorEnum.VALUE_0
    csv_first_row_header: Union[Unset, bool] = True
    filter_user_id: Union[Unset, int] = UNSET
    filter_workspace_id: Union[Unset, int] = UNSET
    filter_action_type: Union[Unset, FilterActionTypeEnum] = UNSET
    filter_from_timestamp: Union[Unset, datetime.datetime] = UNSET
    filter_to_timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_on = self.created_on.isoformat()

        export_charset: Union[Unset, str] = UNSET
        if not isinstance(self.export_charset, Unset):
            export_charset = self.export_charset.value

        csv_column_separator: Union[Unset, str] = UNSET
        if not isinstance(self.csv_column_separator, Unset):
            csv_column_separator = self.csv_column_separator.value

        csv_first_row_header = self.csv_first_row_header
        filter_user_id = self.filter_user_id
        filter_workspace_id = self.filter_workspace_id
        filter_action_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_action_type, Unset):
            filter_action_type = self.filter_action_type.value

        filter_from_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.filter_from_timestamp, Unset):
            filter_from_timestamp = self.filter_from_timestamp.isoformat()

        filter_to_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.filter_to_timestamp, Unset):
            filter_to_timestamp = self.filter_to_timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_on": created_on,
            }
        )
        if export_charset is not UNSET:
            field_dict["export_charset"] = export_charset
        if csv_column_separator is not UNSET:
            field_dict["csv_column_separator"] = csv_column_separator
        if csv_first_row_header is not UNSET:
            field_dict["csv_first_row_header"] = csv_first_row_header
        if filter_user_id is not UNSET:
            field_dict["filter_user_id"] = filter_user_id
        if filter_workspace_id is not UNSET:
            field_dict["filter_workspace_id"] = filter_workspace_id
        if filter_action_type is not UNSET:
            field_dict["filter_action_type"] = filter_action_type
        if filter_from_timestamp is not UNSET:
            field_dict["filter_from_timestamp"] = filter_from_timestamp
        if filter_to_timestamp is not UNSET:
            field_dict["filter_to_timestamp"] = filter_to_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_on = isoparse(d.pop("created_on"))

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

        csv_first_row_header = d.pop("csv_first_row_header", UNSET)

        filter_user_id = d.pop("filter_user_id", UNSET)

        filter_workspace_id = d.pop("filter_workspace_id", UNSET)

        _filter_action_type = d.pop("filter_action_type", UNSET)
        filter_action_type: Union[Unset, FilterActionTypeEnum]
        if isinstance(_filter_action_type, Unset):
            filter_action_type = UNSET
        else:
            filter_action_type = FilterActionTypeEnum(_filter_action_type)

        _filter_from_timestamp = d.pop("filter_from_timestamp", UNSET)
        filter_from_timestamp: Union[Unset, datetime.datetime]
        if isinstance(_filter_from_timestamp, Unset):
            filter_from_timestamp = UNSET
        else:
            filter_from_timestamp = isoparse(_filter_from_timestamp)

        _filter_to_timestamp = d.pop("filter_to_timestamp", UNSET)
        filter_to_timestamp: Union[Unset, datetime.datetime]
        if isinstance(_filter_to_timestamp, Unset):
            filter_to_timestamp = UNSET
        else:
            filter_to_timestamp = isoparse(_filter_to_timestamp)

        single_audit_log_export_job_request = cls(
            created_on=created_on,
            export_charset=export_charset,
            csv_column_separator=csv_column_separator,
            csv_first_row_header=csv_first_row_header,
            filter_user_id=filter_user_id,
            filter_workspace_id=filter_workspace_id,
            filter_action_type=filter_action_type,
            filter_from_timestamp=filter_from_timestamp,
            filter_to_timestamp=filter_to_timestamp,
        )

        single_audit_log_export_job_request.additional_properties = d
        return single_audit_log_export_job_request

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
