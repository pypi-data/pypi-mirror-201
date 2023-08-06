import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.user import User


T = TypeVar("T", bound="Snapshot")


@attr.s(auto_attribs=True)
class Snapshot:
    """
    Attributes:
        id (int):
        name (str):
        snapshot_from_application (int):
        created_by (User):
        created_at (datetime.datetime):
    """

    id: int
    name: str
    snapshot_from_application: int
    created_by: "User"
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        snapshot_from_application = self.snapshot_from_application
        created_by = self.created_by.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "snapshot_from_application": snapshot_from_application,
                "created_by": created_by,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user import User

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        snapshot_from_application = d.pop("snapshot_from_application")

        created_by = User.from_dict(d.pop("created_by"))

        created_at = isoparse(d.pop("created_at"))

        snapshot = cls(
            id=id,
            name=name,
            snapshot_from_application=snapshot_from_application,
            created_by=created_by,
            created_at=created_at,
        )

        snapshot.additional_properties = d
        return snapshot

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
