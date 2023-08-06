from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.row_comment import RowComment


T = TypeVar("T", bound="PaginationSerializerRowComment")


@attr.s(auto_attribs=True)
class PaginationSerializerRowComment:
    """
    Attributes:
        count (int): The total amount of results.
        results (List['RowComment']):
        next_ (Optional[str]): URL to the next page.
        previous (Optional[str]): URL to the previous page.
    """

    count: int
    results: List["RowComment"]
    next_: Optional[str]
    previous: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.row_comment import RowComment

        d = src_dict.copy()
        count = d.pop("count")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = RowComment.from_dict(results_item_data)

            results.append(results_item)

        next_ = d.pop("next")

        previous = d.pop("previous")

        pagination_serializer_row_comment = cls(
            count=count,
            results=results,
            next_=next_,
            previous=previous,
        )

        pagination_serializer_row_comment.additional_properties = d
        return pagination_serializer_row_comment

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
