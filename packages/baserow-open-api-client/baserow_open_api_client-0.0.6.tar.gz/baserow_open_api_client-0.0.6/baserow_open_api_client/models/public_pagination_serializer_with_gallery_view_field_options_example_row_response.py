from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.example_row_response import ExampleRowResponse
    from ..models.public_pagination_serializer_with_gallery_view_field_options_example_row_response_field_options import (
        PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions,
    )


T = TypeVar("T", bound="PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse")


@attr.s(auto_attribs=True)
class PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponse:
    """
    Attributes:
        count (int): The total amount of results.
        results (List['ExampleRowResponse']):
        field_options (Union[Unset,
            PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions]): An object containing the
            field id as key and the properties related to view as value.
        next_ (Optional[str]): URL to the next page.
        previous (Optional[str]): URL to the previous page.
    """

    count: int
    results: List["ExampleRowResponse"]
    next_: Optional[str]
    previous: Optional[str]
    field_options: Union[
        Unset, "PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions"
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        field_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_options, Unset):
            field_options = self.field_options.to_dict()

        next_ = self.next_
        previous = self.previous

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "results": results,
                "next": next_,
                "previous": previous,
            }
        )
        if field_options is not UNSET:
            field_dict["field_options"] = field_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.example_row_response import ExampleRowResponse
        from ..models.public_pagination_serializer_with_gallery_view_field_options_example_row_response_field_options import (
            PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions,
        )

        d = src_dict.copy()
        count = d.pop("count")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = ExampleRowResponse.from_dict(results_item_data)

            results.append(results_item)

        _field_options = d.pop("field_options", UNSET)
        field_options: Union[Unset, PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions]
        if isinstance(_field_options, Unset):
            field_options = UNSET
        else:
            field_options = (
                PublicPaginationSerializerWithGalleryViewFieldOptionsExampleRowResponseFieldOptions.from_dict(
                    _field_options
                )
            )

        next_ = d.pop("next")

        previous = d.pop("previous")

        public_pagination_serializer_with_gallery_view_field_options_example_row_response = cls(
            count=count,
            results=results,
            field_options=field_options,
            next_=next_,
            previous=previous,
        )

        public_pagination_serializer_with_gallery_view_field_options_example_row_response.additional_properties = d
        return public_pagination_serializer_with_gallery_view_field_options_example_row_response

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
