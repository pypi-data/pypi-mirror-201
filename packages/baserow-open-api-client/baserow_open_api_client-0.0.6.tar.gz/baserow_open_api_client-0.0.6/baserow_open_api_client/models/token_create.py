from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenCreate")


@attr.s(auto_attribs=True)
class TokenCreate:
    """A mixin that allows us to rename the `group` field to `workspace` when serializing.

    Attributes:
        name (str): The human readable name of the database token for the user.
        group (str):
        workspace (int): Only the tables of the workspace can be accessed.
    """

    name: str
    group: str
    workspace: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        group = self.group
        workspace = self.workspace

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "group": group,
                "workspace": workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        group = d.pop("group")

        workspace = d.pop("workspace")

        token_create = cls(
            name=name,
            group=group,
            workspace=workspace,
        )

        token_create.additional_properties = d
        return token_create

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
