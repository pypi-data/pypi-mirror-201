from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_7f3_enum import Type7F3Enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestInstallTemplateJobCreateJob")


@attr.s(auto_attribs=True)
class RequestInstallTemplateJobCreateJob:
    """
    Attributes:
        type (Type7F3Enum):
        template_id (int): The template ID that will be installed.
        group_id (Union[Unset, int]): The ID of the group where the template will be installed.
        workspace_id (Union[Unset, int]): The ID of the workspace where the template will be installed.
    """

    type: Type7F3Enum
    template_id: int
    group_id: Union[Unset, int] = UNSET
    workspace_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        template_id = self.template_id
        group_id = self.group_id
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "template_id": template_id,
            }
        )
        if group_id is not UNSET:
            field_dict["group_id"] = group_id
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = Type7F3Enum(d.pop("type"))

        template_id = d.pop("template_id")

        group_id = d.pop("group_id", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        request_install_template_job_create_job = cls(
            type=type,
            template_id=template_id,
            group_id=group_id,
            workspace_id=workspace_id,
        )

        request_install_template_job_create_job.additional_properties = d
        return request_install_template_job_create_job

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
