import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrashContents")


@attr.s(auto_attribs=True)
class TrashContents:
    """
    Attributes:
        id (int):
        user_who_trashed (str):
        trash_item_type (str):
        trash_item_id (int):
        trashed_at (datetime.datetime):
        group (int):
        workspace (int):
        name (str):
        parent_trash_item_id (Union[Unset, None, int]):
        application (Union[Unset, None, int]):
        names (Union[Unset, None, List[str]]):
        parent_name (Union[Unset, None, str]):
    """

    id: int
    user_who_trashed: str
    trash_item_type: str
    trash_item_id: int
    trashed_at: datetime.datetime
    group: int
    workspace: int
    name: str
    parent_trash_item_id: Union[Unset, None, int] = UNSET
    application: Union[Unset, None, int] = UNSET
    names: Union[Unset, None, List[str]] = UNSET
    parent_name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        user_who_trashed = self.user_who_trashed
        trash_item_type = self.trash_item_type
        trash_item_id = self.trash_item_id
        trashed_at = self.trashed_at.isoformat()

        group = self.group
        workspace = self.workspace
        name = self.name
        parent_trash_item_id = self.parent_trash_item_id
        application = self.application
        names: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.names, Unset):
            if self.names is None:
                names = None
            else:
                names = self.names

        parent_name = self.parent_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_who_trashed": user_who_trashed,
                "trash_item_type": trash_item_type,
                "trash_item_id": trash_item_id,
                "trashed_at": trashed_at,
                "group": group,
                "workspace": workspace,
                "name": name,
            }
        )
        if parent_trash_item_id is not UNSET:
            field_dict["parent_trash_item_id"] = parent_trash_item_id
        if application is not UNSET:
            field_dict["application"] = application
        if names is not UNSET:
            field_dict["names"] = names
        if parent_name is not UNSET:
            field_dict["parent_name"] = parent_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        user_who_trashed = d.pop("user_who_trashed")

        trash_item_type = d.pop("trash_item_type")

        trash_item_id = d.pop("trash_item_id")

        trashed_at = isoparse(d.pop("trashed_at"))

        group = d.pop("group")

        workspace = d.pop("workspace")

        name = d.pop("name")

        parent_trash_item_id = d.pop("parent_trash_item_id", UNSET)

        application = d.pop("application", UNSET)

        names = cast(List[str], d.pop("names", UNSET))

        parent_name = d.pop("parent_name", UNSET)

        trash_contents = cls(
            id=id,
            user_who_trashed=user_who_trashed,
            trash_item_type=trash_item_type,
            trash_item_id=trash_item_id,
            trashed_at=trashed_at,
            group=group,
            workspace=workspace,
            name=name,
            parent_trash_item_id=parent_trash_item_id,
            application=application,
            names=names,
            parent_name=parent_name,
        )

        trash_contents.additional_properties = d
        return trash_contents

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
