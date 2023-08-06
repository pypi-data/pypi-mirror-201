from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.application import Application


T = TypeVar("T", bound="AirtableImportJobJob")


@attr.s(auto_attribs=True)
class AirtableImportJobJob:
    """
    Attributes:
        id (int):
        type (str): The type of the job.
        progress_percentage (int): A percentage indicating how far along the job is. 100 means that it's finished.
        state (str): Indicates the state of the import job.
        group_id (int): The group ID where the Airtable base must be imported into.
        workspace_id (int): The workspace ID where the Airtable base must be imported into.
        database (Application):
        airtable_share_id (str): Public ID of the shared Airtable base that must be imported.
        human_readable_error (Union[Unset, str]): A human readable error message indicating what went wrong.
    """

    id: int
    type: str
    progress_percentage: int
    state: str
    group_id: int
    workspace_id: int
    database: "Application"
    airtable_share_id: str
    human_readable_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        progress_percentage = self.progress_percentage
        state = self.state
        group_id = self.group_id
        workspace_id = self.workspace_id
        database = self.database.to_dict()

        airtable_share_id = self.airtable_share_id
        human_readable_error = self.human_readable_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "progress_percentage": progress_percentage,
                "state": state,
                "group_id": group_id,
                "workspace_id": workspace_id,
                "database": database,
                "airtable_share_id": airtable_share_id,
            }
        )
        if human_readable_error is not UNSET:
            field_dict["human_readable_error"] = human_readable_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.application import Application

        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        progress_percentage = d.pop("progress_percentage")

        state = d.pop("state")

        group_id = d.pop("group_id")

        workspace_id = d.pop("workspace_id")

        database = Application.from_dict(d.pop("database"))

        airtable_share_id = d.pop("airtable_share_id")

        human_readable_error = d.pop("human_readable_error", UNSET)

        airtable_import_job_job = cls(
            id=id,
            type=type,
            progress_percentage=progress_percentage,
            state=state,
            group_id=group_id,
            workspace_id=workspace_id,
            database=database,
            airtable_share_id=airtable_share_id,
            human_readable_error=human_readable_error,
        )

        airtable_import_job_job.additional_properties = d
        return airtable_import_job_job

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
