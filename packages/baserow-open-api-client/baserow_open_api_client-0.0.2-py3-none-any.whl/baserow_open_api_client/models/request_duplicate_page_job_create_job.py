from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.type_7f3_enum import Type7F3Enum

T = TypeVar("T", bound="RequestDuplicatePageJobCreateJob")


@attr.s(auto_attribs=True)
class RequestDuplicatePageJobCreateJob:
    """
    Attributes:
        type (Type7F3Enum):
        page_id (int): The ID of the page to duplicate.
    """

    type: Type7F3Enum
    page_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        page_id = self.page_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "page_id": page_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = Type7F3Enum(d.pop("type"))

        page_id = d.pop("page_id")

        request_duplicate_page_job_create_job = cls(
            type=type,
            page_id=page_id,
        )

        request_duplicate_page_job_create_job.additional_properties = d
        return request_duplicate_page_job_create_job

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
