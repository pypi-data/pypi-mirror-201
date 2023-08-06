from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UndoRedoAction")


@attr.s(auto_attribs=True)
class UndoRedoAction:
    """
    Attributes:
        action_type (Union[Unset, None, str]): If an action was undone/redone/skipped due to an error this field will
            contain the type of the action that was undone/redone.
        action_scope (Union[Unset, None, str]): If an action was undone/redone/skipped due to an error this field will
            contain the scope of the action that was undone/redone.
    """

    action_type: Union[Unset, None, str] = UNSET
    action_scope: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action_type = self.action_type
        action_scope = self.action_scope

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if action_scope is not UNSET:
            field_dict["action_scope"] = action_scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action_type = d.pop("action_type", UNSET)

        action_scope = d.pop("action_scope", UNSET)

        undo_redo_action = cls(
            action_type=action_type,
            action_scope=action_scope,
        )

        undo_redo_action.additional_properties = d
        return undo_redo_action

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
