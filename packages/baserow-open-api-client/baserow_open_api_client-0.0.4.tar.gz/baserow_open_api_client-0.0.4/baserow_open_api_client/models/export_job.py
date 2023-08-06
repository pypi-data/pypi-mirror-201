import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.state_enum import StateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportJob")


@attr.s(auto_attribs=True)
class ExportJob:
    """When mixed in to a model serializer for an ExportJob this will add an url field
    with the actual usable url of the export job's file (if it has one).

        Attributes:
            id (int):
            exporter_type (str):
            state (StateEnum):
            status (str): DEPRECATED: Use state instead
            created_at (datetime.datetime):
            url (str):
            table (Union[Unset, None, int]):
            view (Union[Unset, None, int]):
            exported_file_name (Union[Unset, None, str]):
            progress_percentage (Union[Unset, float]):
    """

    id: int
    exporter_type: str
    state: StateEnum
    status: str
    created_at: datetime.datetime
    url: str
    table: Union[Unset, None, int] = UNSET
    view: Union[Unset, None, int] = UNSET
    exported_file_name: Union[Unset, None, str] = UNSET
    progress_percentage: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        exporter_type = self.exporter_type
        state = self.state.value

        status = self.status
        created_at = self.created_at.isoformat()

        url = self.url
        table = self.table
        view = self.view
        exported_file_name = self.exported_file_name
        progress_percentage = self.progress_percentage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "exporter_type": exporter_type,
                "state": state,
                "status": status,
                "created_at": created_at,
                "url": url,
            }
        )
        if table is not UNSET:
            field_dict["table"] = table
        if view is not UNSET:
            field_dict["view"] = view
        if exported_file_name is not UNSET:
            field_dict["exported_file_name"] = exported_file_name
        if progress_percentage is not UNSET:
            field_dict["progress_percentage"] = progress_percentage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        exporter_type = d.pop("exporter_type")

        state = StateEnum(d.pop("state"))

        status = d.pop("status")

        created_at = isoparse(d.pop("created_at"))

        url = d.pop("url")

        table = d.pop("table", UNSET)

        view = d.pop("view", UNSET)

        exported_file_name = d.pop("exported_file_name", UNSET)

        progress_percentage = d.pop("progress_percentage", UNSET)

        export_job = cls(
            id=id,
            exporter_type=exporter_type,
            state=state,
            status=status,
            created_at=created_at,
            url=url,
            table=table,
            view=view,
            exported_file_name=exported_file_name,
            progress_percentage=progress_percentage,
        )

        export_job.additional_properties = d
        return export_job

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
