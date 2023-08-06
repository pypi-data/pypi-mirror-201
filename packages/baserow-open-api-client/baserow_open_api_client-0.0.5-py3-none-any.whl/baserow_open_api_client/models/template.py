from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Template")


@attr.s(auto_attribs=True)
class Template:
    """
    Attributes:
        id (int):
        name (str):
        icon (str): The font awesome class name that can be used for displaying purposes.
        group_id (str):
        is_default (str): Indicates if the template must be selected by default. The web-frontend automatically selects
            the first `is_default` template that it can find.
        keywords (Union[Unset, str]): Keywords related to the template that can be used for search.
        workspace_id (Optional[int]): The group containing the applications related to the template. The read endpoints
            related to that group are publicly accessible for preview purposes.
    """

    id: int
    name: str
    icon: str
    group_id: str
    is_default: str
    workspace_id: Optional[int]
    keywords: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        icon = self.icon
        group_id = self.group_id
        is_default = self.is_default
        keywords = self.keywords
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "icon": icon,
                "group_id": group_id,
                "is_default": is_default,
                "workspace_id": workspace_id,
            }
        )
        if keywords is not UNSET:
            field_dict["keywords"] = keywords

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        icon = d.pop("icon")

        group_id = d.pop("group_id")

        is_default = d.pop("is_default")

        keywords = d.pop("keywords", UNSET)

        workspace_id = d.pop("workspace_id")

        template = cls(
            id=id,
            name=name,
            icon=icon,
            group_id=group_id,
            is_default=is_default,
            keywords=keywords,
            workspace_id=workspace_id,
        )

        template.additional_properties = d
        return template

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
