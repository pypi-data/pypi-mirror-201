from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report import Report


T = TypeVar("T", bound="FileImportJobJob")


@attr.s(auto_attribs=True)
class FileImportJobJob:
    """
    Attributes:
        id (int):
        type (str): The type of the job.
        progress_percentage (int): A percentage indicating how far along the job is. 100 means that it's finished.
        state (str): Indicates the state of the import job.
        database_id (int): Database id where the table will be created.
        report (Report):
        human_readable_error (Union[Unset, str]): A human readable error message indicating what went wrong.
        name (Union[Unset, str]): The name of the new table.
        table_id (Union[Unset, int]): Table id where the data will be imported.
        first_row_header (Union[Unset, bool]):
    """

    id: int
    type: str
    progress_percentage: int
    state: str
    database_id: int
    report: "Report"
    human_readable_error: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    table_id: Union[Unset, int] = UNSET
    first_row_header: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        progress_percentage = self.progress_percentage
        state = self.state
        database_id = self.database_id
        report = self.report.to_dict()

        human_readable_error = self.human_readable_error
        name = self.name
        table_id = self.table_id
        first_row_header = self.first_row_header

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "progress_percentage": progress_percentage,
                "state": state,
                "database_id": database_id,
                "report": report,
            }
        )
        if human_readable_error is not UNSET:
            field_dict["human_readable_error"] = human_readable_error
        if name is not UNSET:
            field_dict["name"] = name
        if table_id is not UNSET:
            field_dict["table_id"] = table_id
        if first_row_header is not UNSET:
            field_dict["first_row_header"] = first_row_header

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report import Report

        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        progress_percentage = d.pop("progress_percentage")

        state = d.pop("state")

        database_id = d.pop("database_id")

        report = Report.from_dict(d.pop("report"))

        human_readable_error = d.pop("human_readable_error", UNSET)

        name = d.pop("name", UNSET)

        table_id = d.pop("table_id", UNSET)

        first_row_header = d.pop("first_row_header", UNSET)

        file_import_job_job = cls(
            id=id,
            type=type,
            progress_percentage=progress_percentage,
            state=state,
            database_id=database_id,
            report=report,
            human_readable_error=human_readable_error,
            name=name,
            table_id=table_id,
            first_row_header=first_row_header,
        )

        file_import_job_job.additional_properties = d
        return file_import_job_job

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
