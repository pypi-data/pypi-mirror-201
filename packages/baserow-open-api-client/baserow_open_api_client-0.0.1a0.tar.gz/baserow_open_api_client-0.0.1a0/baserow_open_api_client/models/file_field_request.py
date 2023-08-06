from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileFieldRequest")


@attr.s(auto_attribs=True)
class FileFieldRequest:
    """
    Attributes:
        name (str): Accepts the name of the already uploaded user file.
        visible_name (Union[Unset, str]): A visually editable name for the field.
    """

    name: str
    visible_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        visible_name = self.visible_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if visible_name is not UNSET:
            field_dict["visible_name"] = visible_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        visible_name = d.pop("visible_name", UNSET)

        file_field_request = cls(
            name=name,
            visible_name=visible_name,
        )

        file_field_request.additional_properties = d
        return file_field_request

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
