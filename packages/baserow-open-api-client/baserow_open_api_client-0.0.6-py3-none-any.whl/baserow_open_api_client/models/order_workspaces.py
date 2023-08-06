from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="OrderWorkspaces")


@attr.s(auto_attribs=True)
class OrderWorkspaces:
    """
    Attributes:
        workspaces (List[int]): Workspace ids in the desired order.
    """

    workspaces: List[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspaces = self.workspaces

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspaces": workspaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspaces = cast(List[int], d.pop("workspaces"))

        order_workspaces = cls(
            workspaces=workspaces,
        )

        order_workspaces.additional_properties = d
        return order_workspaces

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
