from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.single_install_template_job_type_installed_applications import (
        SingleInstallTemplateJobTypeInstalledApplications,
    )
    from ..models.template import Template
    from ..models.workspace import Workspace


T = TypeVar("T", bound="SingleInstallTemplateJobType")


@attr.s(auto_attribs=True)
class SingleInstallTemplateJobType:
    """
    Attributes:
        id (int):
        type (str): The type of the job.
        progress_percentage (int): A percentage indicating how far along the job is. 100 means that it's finished.
        state (str): Indicates the state of the import job.
        workspace (Workspace):
        template (Template):
        installed_applications (SingleInstallTemplateJobTypeInstalledApplications):
        group (Workspace):
        human_readable_error (Union[Unset, str]): A human readable error message indicating what went wrong.
    """

    id: int
    type: str
    progress_percentage: int
    state: str
    workspace: "Workspace"
    template: "Template"
    installed_applications: "SingleInstallTemplateJobTypeInstalledApplications"
    group: "Workspace"
    human_readable_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        type = self.type
        progress_percentage = self.progress_percentage
        state = self.state
        workspace = self.workspace.to_dict()

        template = self.template.to_dict()

        installed_applications = self.installed_applications.to_dict()

        group = self.group.to_dict()

        human_readable_error = self.human_readable_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "progress_percentage": progress_percentage,
                "state": state,
                "workspace": workspace,
                "template": template,
                "installed_applications": installed_applications,
                "group": group,
            }
        )
        if human_readable_error is not UNSET:
            field_dict["human_readable_error"] = human_readable_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.single_install_template_job_type_installed_applications import (
            SingleInstallTemplateJobTypeInstalledApplications,
        )
        from ..models.template import Template
        from ..models.workspace import Workspace

        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        progress_percentage = d.pop("progress_percentage")

        state = d.pop("state")

        workspace = Workspace.from_dict(d.pop("workspace"))

        template = Template.from_dict(d.pop("template"))

        installed_applications = SingleInstallTemplateJobTypeInstalledApplications.from_dict(
            d.pop("installed_applications")
        )

        group = Workspace.from_dict(d.pop("group"))

        human_readable_error = d.pop("human_readable_error", UNSET)

        single_install_template_job_type = cls(
            id=id,
            type=type,
            progress_percentage=progress_percentage,
            state=state,
            workspace=workspace,
            template=template,
            installed_applications=installed_applications,
            group=group,
            human_readable_error=human_readable_error,
        )

        single_install_template_job_type.additional_properties = d
        return single_install_template_job_type

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
