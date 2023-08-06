from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.gallery_view_field_options import GalleryViewFieldOptions


T = TypeVar("T", bound="PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions")


@attr.s(auto_attribs=True)
class PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions:
    """An object containing the field id as key and the properties related to view as value."""

    additional_properties: Dict[str, "GalleryViewFieldOptions"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.gallery_view_field_options import GalleryViewFieldOptions

        d = src_dict.copy()
        public_pagination_serializer_with_gallery_view_field_options_example_row_response_field_options = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GalleryViewFieldOptions.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        public_pagination_serializer_with_gallery_view_field_options_example_row_response_field_options.additional_properties = (
            additional_properties
        )
        return public_pagination_serializer_with_gallery_view_field_options_example_row_response_field_options

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GalleryViewFieldOptions":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GalleryViewFieldOptions") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
