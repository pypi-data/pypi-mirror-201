from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page_path_params import PagePathParams


T = TypeVar("T", bound="Page")


@attr.s(auto_attribs=True)
class Page:
    """
    Attributes:
        id (int):
        name (str):
        path (str):
        order (int): Lowest first.
        builder_id (int):
        path_params (Union[Unset, PagePathParams]):
    """

    id: int
    name: str
    path: str
    order: int
    builder_id: int
    path_params: Union[Unset, "PagePathParams"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        path = self.path
        order = self.order
        builder_id = self.builder_id
        path_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.path_params, Unset):
            path_params = self.path_params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "path": path,
                "order": order,
                "builder_id": builder_id,
            }
        )
        if path_params is not UNSET:
            field_dict["path_params"] = path_params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page_path_params import PagePathParams

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        path = d.pop("path")

        order = d.pop("order")

        builder_id = d.pop("builder_id")

        _path_params = d.pop("path_params", UNSET)
        path_params: Union[Unset, PagePathParams]
        if isinstance(_path_params, Unset):
            path_params = UNSET
        else:
            path_params = PagePathParams.from_dict(_path_params)

        page = cls(
            id=id,
            name=name,
            path=path,
            order=order,
            builder_id=builder_id,
            path_params=path_params,
        )

        page.additional_properties = d
        return page

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
