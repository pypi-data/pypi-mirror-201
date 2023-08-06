from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.application_create_type_enum import ApplicationCreateTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationCreate")


@attr.s(auto_attribs=True)
class ApplicationCreate:
    """
    Attributes:
        name (str):
        type (ApplicationCreateTypeEnum):
        init_with_data (Union[Unset, bool]):
    """

    name: str
    type: ApplicationCreateTypeEnum
    init_with_data: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        init_with_data = self.init_with_data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
            }
        )
        if init_with_data is not UNSET:
            field_dict["init_with_data"] = init_with_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = ApplicationCreateTypeEnum(d.pop("type"))

        init_with_data = d.pop("init_with_data", UNSET)

        application_create = cls(
            name=name,
            type=type,
            init_with_data=init_with_data,
        )

        application_create.additional_properties = d
        return application_create

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
