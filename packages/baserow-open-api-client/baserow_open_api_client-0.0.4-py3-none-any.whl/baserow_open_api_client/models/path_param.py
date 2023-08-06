from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.param_type_enum import ParamTypeEnum

T = TypeVar("T", bound="PathParam")


@attr.s(auto_attribs=True)
class PathParam:
    """
    Attributes:
        param_type (ParamTypeEnum):
    """

    param_type: ParamTypeEnum
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        param_type = self.param_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "param_type": param_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        param_type = ParamTypeEnum(d.pop("param_type"))

        path_param = cls(
            param_type=param_type,
        )

        path_param.additional_properties = d
        return path_param

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
