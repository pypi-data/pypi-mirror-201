import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="AuditLog")


@attr.s(auto_attribs=True)
class AuditLog:
    """
    Attributes:
        id (int):
        action_type (str):
        user (str):
        group (str):
        workspace (str):
        type (str):
        description (str):
        timestamp (datetime.datetime):
        ip_address (Optional[str]):
    """

    id: int
    action_type: str
    user: str
    group: str
    workspace: str
    type: str
    description: str
    timestamp: datetime.datetime
    ip_address: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        action_type = self.action_type
        user = self.user
        group = self.group
        workspace = self.workspace
        type = self.type
        description = self.description
        timestamp = self.timestamp.isoformat()

        ip_address = self.ip_address

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "action_type": action_type,
                "user": user,
                "group": group,
                "workspace": workspace,
                "type": type,
                "description": description,
                "timestamp": timestamp,
                "ip_address": ip_address,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        action_type = d.pop("action_type")

        user = d.pop("user")

        group = d.pop("group")

        workspace = d.pop("workspace")

        type = d.pop("type")

        description = d.pop("description")

        timestamp = isoparse(d.pop("timestamp"))

        ip_address = d.pop("ip_address")

        audit_log = cls(
            id=id,
            action_type=action_type,
            user=user,
            group=group,
            workspace=workspace,
            type=type,
            description=description,
            timestamp=timestamp,
            ip_address=ip_address,
        )

        audit_log.additional_properties = d
        return audit_log

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
