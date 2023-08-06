from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.path_param import PathParam


T = TypeVar("T", bound="PatchedUpdatePagePathParams")


@attr.s(auto_attribs=True)
class PatchedUpdatePagePathParams:
    """ """

    additional_properties: Dict[str, "PathParam"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.path_param import PathParam

        d = src_dict.copy()
        patched_update_page_path_params = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PathParam.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        patched_update_page_path_params.additional_properties = additional_properties
        return patched_update_page_path_params

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "PathParam":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "PathParam") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
