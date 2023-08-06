import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="AdminDashboardPerDay")


@attr.s(auto_attribs=True)
class AdminDashboardPerDay:
    """
    Attributes:
        date (datetime.date):
        count (int):
    """

    date: datetime.date
    count: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date = self.date.isoformat()
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        date = isoparse(d.pop("date")).date()

        count = d.pop("count")

        admin_dashboard_per_day = cls(
            date=date,
            count=count,
        )

        admin_dashboard_per_day.additional_properties = d
        return admin_dashboard_per_day

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
