from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_page_path_params import CreatePagePathParams


T = TypeVar("T", bound="CreatePage")


@attr.s(auto_attribs=True)
class CreatePage:
    """
    Attributes:
        name (str):
        path (str):
        path_params (Union[Unset, CreatePagePathParams]):
    """

    name: str
    path: str
    path_params: Union[Unset, "CreatePagePathParams"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        path = self.path
        path_params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.path_params, Unset):
            path_params = self.path_params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "path": path,
            }
        )
        if path_params is not UNSET:
            field_dict["path_params"] = path_params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_page_path_params import CreatePagePathParams

        d = src_dict.copy()
        name = d.pop("name")

        path = d.pop("path")

        _path_params = d.pop("path_params", UNSET)
        path_params: Union[Unset, CreatePagePathParams]
        if isinstance(_path_params, Unset):
            path_params = UNSET
        else:
            path_params = CreatePagePathParams.from_dict(_path_params)

        create_page = cls(
            name=name,
            path=path,
            path_params=path_params,
        )

        create_page.additional_properties = d
        return create_page

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
