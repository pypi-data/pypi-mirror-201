from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.row_metadata import RowMetadata


T = TypeVar("T", bound="PaginationSerializerWithGridViewFieldOptionsExampleRowResponseRowMetadata")


@attr.s(auto_attribs=True)
class PaginationSerializerWithGridViewFieldOptionsExampleRowResponseRowMetadata:
    """An object keyed by row id with a value being an object containing additional metadata about that row. A row might
    not have metadata and will not be present as a key if so.

    """

    additional_properties: Dict[str, "RowMetadata"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.row_metadata import RowMetadata

        d = src_dict.copy()
        pagination_serializer_with_grid_view_field_options_example_row_response_row_metadata = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RowMetadata.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        pagination_serializer_with_grid_view_field_options_example_row_response_row_metadata.additional_properties = (
            additional_properties
        )
        return pagination_serializer_with_grid_view_field_options_example_row_response_row_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "RowMetadata":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "RowMetadata") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
