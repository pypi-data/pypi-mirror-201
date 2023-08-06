from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.admin_dashboard_per_day import AdminDashboardPerDay


T = TypeVar("T", bound="AdminDashboard")


@attr.s(auto_attribs=True)
class AdminDashboard:
    """
    Attributes:
        total_users (int):
        total_groups (int):
        total_workspaces (int):
        total_applications (int):
        new_users_last_24_hours (int):
        new_users_last_7_days (int):
        new_users_last_30_days (int):
        previous_new_users_last_24_hours (int):
        previous_new_users_last_7_days (int):
        previous_new_users_last_30_days (int):
        active_users_last_24_hours (int):
        active_users_last_7_days (int):
        active_users_last_30_days (int):
        previous_active_users_last_24_hours (int):
        previous_active_users_last_7_days (int):
        previous_active_users_last_30_days (int):
        new_users_per_day (List['AdminDashboardPerDay']):
        active_users_per_day (List['AdminDashboardPerDay']):
    """

    total_users: int
    total_groups: int
    total_workspaces: int
    total_applications: int
    new_users_last_24_hours: int
    new_users_last_7_days: int
    new_users_last_30_days: int
    previous_new_users_last_24_hours: int
    previous_new_users_last_7_days: int
    previous_new_users_last_30_days: int
    active_users_last_24_hours: int
    active_users_last_7_days: int
    active_users_last_30_days: int
    previous_active_users_last_24_hours: int
    previous_active_users_last_7_days: int
    previous_active_users_last_30_days: int
    new_users_per_day: List["AdminDashboardPerDay"]
    active_users_per_day: List["AdminDashboardPerDay"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_users = self.total_users
        total_groups = self.total_groups
        total_workspaces = self.total_workspaces
        total_applications = self.total_applications
        new_users_last_24_hours = self.new_users_last_24_hours
        new_users_last_7_days = self.new_users_last_7_days
        new_users_last_30_days = self.new_users_last_30_days
        previous_new_users_last_24_hours = self.previous_new_users_last_24_hours
        previous_new_users_last_7_days = self.previous_new_users_last_7_days
        previous_new_users_last_30_days = self.previous_new_users_last_30_days
        active_users_last_24_hours = self.active_users_last_24_hours
        active_users_last_7_days = self.active_users_last_7_days
        active_users_last_30_days = self.active_users_last_30_days
        previous_active_users_last_24_hours = self.previous_active_users_last_24_hours
        previous_active_users_last_7_days = self.previous_active_users_last_7_days
        previous_active_users_last_30_days = self.previous_active_users_last_30_days
        new_users_per_day = []
        for new_users_per_day_item_data in self.new_users_per_day:
            new_users_per_day_item = new_users_per_day_item_data.to_dict()

            new_users_per_day.append(new_users_per_day_item)

        active_users_per_day = []
        for active_users_per_day_item_data in self.active_users_per_day:
            active_users_per_day_item = active_users_per_day_item_data.to_dict()

            active_users_per_day.append(active_users_per_day_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_users": total_users,
                "total_groups": total_groups,
                "total_workspaces": total_workspaces,
                "total_applications": total_applications,
                "new_users_last_24_hours": new_users_last_24_hours,
                "new_users_last_7_days": new_users_last_7_days,
                "new_users_last_30_days": new_users_last_30_days,
                "previous_new_users_last_24_hours": previous_new_users_last_24_hours,
                "previous_new_users_last_7_days": previous_new_users_last_7_days,
                "previous_new_users_last_30_days": previous_new_users_last_30_days,
                "active_users_last_24_hours": active_users_last_24_hours,
                "active_users_last_7_days": active_users_last_7_days,
                "active_users_last_30_days": active_users_last_30_days,
                "previous_active_users_last_24_hours": previous_active_users_last_24_hours,
                "previous_active_users_last_7_days": previous_active_users_last_7_days,
                "previous_active_users_last_30_days": previous_active_users_last_30_days,
                "new_users_per_day": new_users_per_day,
                "active_users_per_day": active_users_per_day,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.admin_dashboard_per_day import AdminDashboardPerDay

        d = src_dict.copy()
        total_users = d.pop("total_users")

        total_groups = d.pop("total_groups")

        total_workspaces = d.pop("total_workspaces")

        total_applications = d.pop("total_applications")

        new_users_last_24_hours = d.pop("new_users_last_24_hours")

        new_users_last_7_days = d.pop("new_users_last_7_days")

        new_users_last_30_days = d.pop("new_users_last_30_days")

        previous_new_users_last_24_hours = d.pop("previous_new_users_last_24_hours")

        previous_new_users_last_7_days = d.pop("previous_new_users_last_7_days")

        previous_new_users_last_30_days = d.pop("previous_new_users_last_30_days")

        active_users_last_24_hours = d.pop("active_users_last_24_hours")

        active_users_last_7_days = d.pop("active_users_last_7_days")

        active_users_last_30_days = d.pop("active_users_last_30_days")

        previous_active_users_last_24_hours = d.pop("previous_active_users_last_24_hours")

        previous_active_users_last_7_days = d.pop("previous_active_users_last_7_days")

        previous_active_users_last_30_days = d.pop("previous_active_users_last_30_days")

        new_users_per_day = []
        _new_users_per_day = d.pop("new_users_per_day")
        for new_users_per_day_item_data in _new_users_per_day:
            new_users_per_day_item = AdminDashboardPerDay.from_dict(new_users_per_day_item_data)

            new_users_per_day.append(new_users_per_day_item)

        active_users_per_day = []
        _active_users_per_day = d.pop("active_users_per_day")
        for active_users_per_day_item_data in _active_users_per_day:
            active_users_per_day_item = AdminDashboardPerDay.from_dict(active_users_per_day_item_data)

            active_users_per_day.append(active_users_per_day_item)

        admin_dashboard = cls(
            total_users=total_users,
            total_groups=total_groups,
            total_workspaces=total_workspaces,
            total_applications=total_applications,
            new_users_last_24_hours=new_users_last_24_hours,
            new_users_last_7_days=new_users_last_7_days,
            new_users_last_30_days=new_users_last_30_days,
            previous_new_users_last_24_hours=previous_new_users_last_24_hours,
            previous_new_users_last_7_days=previous_new_users_last_7_days,
            previous_new_users_last_30_days=previous_new_users_last_30_days,
            active_users_last_24_hours=active_users_last_24_hours,
            active_users_last_7_days=active_users_last_7_days,
            active_users_last_30_days=active_users_last_30_days,
            previous_active_users_last_24_hours=previous_active_users_last_24_hours,
            previous_active_users_last_7_days=previous_active_users_last_7_days,
            previous_active_users_last_30_days=previous_active_users_last_30_days,
            new_users_per_day=new_users_per_day,
            active_users_per_day=active_users_per_day,
        )

        admin_dashboard.additional_properties = d
        return admin_dashboard

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
