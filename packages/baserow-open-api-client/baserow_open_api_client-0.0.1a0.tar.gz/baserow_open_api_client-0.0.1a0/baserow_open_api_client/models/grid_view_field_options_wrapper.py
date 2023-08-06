from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.grid_view_field_options_wrapper_field_options import GridViewFieldOptionsWrapperFieldOptions


T = TypeVar("T", bound="GridViewFieldOptionsWrapper")


@attr.s(auto_attribs=True)
class GridViewFieldOptionsWrapper:
    """
    Attributes:
        field_options (GridViewFieldOptionsWrapperFieldOptions): An object containing the field id as key and the
            properties related to view as value.
    """

    field_options: "GridViewFieldOptionsWrapperFieldOptions"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_options = self.field_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field_options": field_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.grid_view_field_options_wrapper_field_options import GridViewFieldOptionsWrapperFieldOptions

        d = src_dict.copy()
        field_options = GridViewFieldOptionsWrapperFieldOptions.from_dict(d.pop("field_options"))

        grid_view_field_options_wrapper = cls(
            field_options=field_options,
        )

        grid_view_field_options_wrapper.additional_properties = d
        return grid_view_field_options_wrapper

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
