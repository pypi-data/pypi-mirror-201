from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.undo_redo_action import UndoRedoAction


T = TypeVar("T", bound="UndoRedoResponse")


@attr.s(auto_attribs=True)
class UndoRedoResponse:
    """
    Attributes:
        actions (List['UndoRedoAction']):
        result_code (str): Indicates the result of the undo/redo operation. Will be 'SUCCESS' on success,
            'NOTHING_TO_DO' when there is no action to undo/redo and 'SKIPPED_DUE_TO_ERROR' when the undo/redo failed due to
            a conflict or error and was skipped over.
    """

    actions: List["UndoRedoAction"]
    result_code: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        result_code = self.result_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actions": actions,
                "result_code": result_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.undo_redo_action import UndoRedoAction

        d = src_dict.copy()
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = UndoRedoAction.from_dict(actions_item_data)

            actions.append(actions_item)

        result_code = d.pop("result_code")

        undo_redo_response = cls(
            actions=actions,
            result_code=result_code,
        )

        undo_redo_response.additional_properties = d
        return undo_redo_response

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
