from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.trash_item_type_enum import TrashItemTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTrashEntryRequest")


@attr.s(auto_attribs=True)
class PatchedTrashEntryRequest:
    """Mixin to a DRF serializer class to raise an exception if data with unknown fields
    is provided to the serializer.

        Attributes:
            trash_item_id (Union[Unset, int]):
            parent_trash_item_id (Union[Unset, None, int]):
            trash_item_type (Union[Unset, TrashItemTypeEnum]):
    """

    trash_item_id: Union[Unset, int] = UNSET
    parent_trash_item_id: Union[Unset, None, int] = UNSET
    trash_item_type: Union[Unset, TrashItemTypeEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trash_item_id = self.trash_item_id
        parent_trash_item_id = self.parent_trash_item_id
        trash_item_type: Union[Unset, str] = UNSET
        if not isinstance(self.trash_item_type, Unset):
            trash_item_type = self.trash_item_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trash_item_id is not UNSET:
            field_dict["trash_item_id"] = trash_item_id
        if parent_trash_item_id is not UNSET:
            field_dict["parent_trash_item_id"] = parent_trash_item_id
        if trash_item_type is not UNSET:
            field_dict["trash_item_type"] = trash_item_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trash_item_id = d.pop("trash_item_id", UNSET)

        parent_trash_item_id = d.pop("parent_trash_item_id", UNSET)

        _trash_item_type = d.pop("trash_item_type", UNSET)
        trash_item_type: Union[Unset, TrashItemTypeEnum]
        if isinstance(_trash_item_type, Unset):
            trash_item_type = UNSET
        else:
            trash_item_type = TrashItemTypeEnum(_trash_item_type)

        patched_trash_entry_request = cls(
            trash_item_id=trash_item_id,
            parent_trash_item_id=parent_trash_item_id,
            trash_item_type=trash_item_type,
        )

        patched_trash_entry_request.additional_properties = d
        return patched_trash_entry_request

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
