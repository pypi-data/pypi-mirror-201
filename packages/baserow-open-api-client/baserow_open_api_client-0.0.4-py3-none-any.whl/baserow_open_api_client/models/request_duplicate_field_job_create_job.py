from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.type_7f3_enum import Type7F3Enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestDuplicateFieldJobCreateJob")


@attr.s(auto_attribs=True)
class RequestDuplicateFieldJobCreateJob:
    """
    Attributes:
        type (Type7F3Enum):
        field_id (int): The ID of the field to duplicate.
        duplicate_data (Union[Unset, bool]): Whether to duplicate the data of the field.
    """

    type: Type7F3Enum
    field_id: int
    duplicate_data: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_id = self.field_id
        duplicate_data = self.duplicate_data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "field_id": field_id,
            }
        )
        if duplicate_data is not UNSET:
            field_dict["duplicate_data"] = duplicate_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = Type7F3Enum(d.pop("type"))

        field_id = d.pop("field_id")

        duplicate_data = d.pop("duplicate_data", UNSET)

        request_duplicate_field_job_create_job = cls(
            type=type,
            field_id=field_id,
            duplicate_data=duplicate_data,
        )

        request_duplicate_field_job_create_job.additional_properties = d
        return request_duplicate_field_job_create_job

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
