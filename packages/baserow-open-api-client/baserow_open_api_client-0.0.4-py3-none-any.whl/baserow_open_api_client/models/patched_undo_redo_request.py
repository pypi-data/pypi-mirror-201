from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action_scopes import ActionScopes


T = TypeVar("T", bound="PatchedUndoRedoRequest")


@attr.s(auto_attribs=True)
class PatchedUndoRedoRequest:
    """
    Attributes:
        scopes (Union[Unset, ActionScopes]): Mixin to a DRF serializer class to raise an exception if data with unknown
            fields
            is provided to the serializer.
    """

    scopes: Union[Unset, "ActionScopes"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scopes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.action_scopes import ActionScopes

        d = src_dict.copy()
        _scopes = d.pop("scopes", UNSET)
        scopes: Union[Unset, ActionScopes]
        if isinstance(_scopes, Unset):
            scopes = UNSET
        else:
            scopes = ActionScopes.from_dict(_scopes)

        patched_undo_redo_request = cls(
            scopes=scopes,
        )

        patched_undo_redo_request.additional_properties = d
        return patched_undo_redo_request

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
