from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.public_view_sort import PublicViewSort
    from ..models.public_view_table import PublicViewTable


T = TypeVar("T", bound="PublicView")


@attr.s(auto_attribs=True)
class PublicView:
    """
    Attributes:
        id (str):
        table (PublicViewTable):
        name (str):
        order (int):
        type (str):
        sortings (List['PublicViewSort']):
        slug (str): The unique slug where the view can be accessed publicly on.
        public (Union[Unset, bool]): Indicates whether the view is publicly accessible to visitors.
        show_logo (Union[Unset, bool]):
    """

    id: str
    table: "PublicViewTable"
    name: str
    order: int
    type: str
    sortings: List["PublicViewSort"]
    slug: str
    public: Union[Unset, bool] = UNSET
    show_logo: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table = self.table.to_dict()

        name = self.name
        order = self.order
        type = self.type
        sortings = []
        for sortings_item_data in self.sortings:
            sortings_item = sortings_item_data.to_dict()

            sortings.append(sortings_item)

        slug = self.slug
        public = self.public
        show_logo = self.show_logo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table": table,
                "name": name,
                "order": order,
                "type": type,
                "sortings": sortings,
                "slug": slug,
            }
        )
        if public is not UNSET:
            field_dict["public"] = public
        if show_logo is not UNSET:
            field_dict["show_logo"] = show_logo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.public_view_sort import PublicViewSort
        from ..models.public_view_table import PublicViewTable

        d = src_dict.copy()
        id = d.pop("id")

        table = PublicViewTable.from_dict(d.pop("table"))

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        sortings = []
        _sortings = d.pop("sortings")
        for sortings_item_data in _sortings:
            sortings_item = PublicViewSort.from_dict(sortings_item_data)

            sortings.append(sortings_item)

        slug = d.pop("slug")

        public = d.pop("public", UNSET)

        show_logo = d.pop("show_logo", UNSET)

        public_view = cls(
            id=id,
            table=table,
            name=name,
            order=order,
            type=type,
            sortings=sortings,
            slug=slug,
            public=public,
            show_logo=show_logo,
        )

        public_view.additional_properties = d
        return public_view

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
