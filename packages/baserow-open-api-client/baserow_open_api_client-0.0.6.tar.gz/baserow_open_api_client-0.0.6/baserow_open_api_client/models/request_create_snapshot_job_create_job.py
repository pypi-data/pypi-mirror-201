from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.type_7f3_enum import Type7F3Enum

T = TypeVar("T", bound="RequestCreateSnapshotJobCreateJob")


@attr.s(auto_attribs=True)
class RequestCreateSnapshotJobCreateJob:
    """
    Attributes:
        type (Type7F3Enum):
    """

    type: Type7F3Enum
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = Type7F3Enum(d.pop("type"))

        request_create_snapshot_job_create_job = cls(
            type=type,
        )

        request_create_snapshot_job_create_job.additional_properties = d
        return request_create_snapshot_job_create_job

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
