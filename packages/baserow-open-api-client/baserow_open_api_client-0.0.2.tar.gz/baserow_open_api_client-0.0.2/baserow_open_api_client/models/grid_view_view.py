from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..models.row_identifier_type_enum import RowIdentifierTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table import Table
    from ..models.view_decoration import ViewDecoration
    from ..models.view_filter import ViewFilter
    from ..models.view_sort import ViewSort


T = TypeVar("T", bound="GridViewView")


@attr.s(auto_attribs=True)
class GridViewView:
    """
    Attributes:
        id (int):
        table_id (int):
        name (str):
        order (int):
        type (str):
        table (Table):
        public_view_has_password (bool):
        ownership_type (str):
        slug (str): The unique slug that can be used to construct a public URL.
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters (Union[Unset, List['ViewFilter']]):
        sortings (Union[Unset, List['ViewSort']]):
        decorations (Union[Unset, List['ViewDecoration']]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
        show_logo (Union[Unset, bool]):
        row_identifier_type (Union[Unset, RowIdentifierTypeEnum]):
        public (Union[Unset, bool]): Indicates whether the view is publicly accessible to visitors.
    """

    id: int
    table_id: int
    name: str
    order: int
    type: str
    table: "Table"
    public_view_has_password: bool
    ownership_type: str
    slug: str
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters: Union[Unset, List["ViewFilter"]] = UNSET
    sortings: Union[Unset, List["ViewSort"]] = UNSET
    decorations: Union[Unset, List["ViewDecoration"]] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
    show_logo: Union[Unset, bool] = UNSET
    row_identifier_type: Union[Unset, RowIdentifierTypeEnum] = UNSET
    public: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        name = self.name
        order = self.order
        type = self.type
        table = self.table.to_dict()

        public_view_has_password = self.public_view_has_password
        ownership_type = self.ownership_type
        slug = self.slug
        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sortings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sortings, Unset):
            sortings = []
            for sortings_item_data in self.sortings:
                sortings_item = sortings_item_data.to_dict()

                sortings.append(sortings_item)

        decorations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.decorations, Unset):
            decorations = []
            for decorations_item_data in self.decorations:
                decorations_item = decorations_item_data.to_dict()

                decorations.append(decorations_item)

        filters_disabled = self.filters_disabled
        show_logo = self.show_logo
        row_identifier_type: Union[Unset, str] = UNSET
        if not isinstance(self.row_identifier_type, Unset):
            row_identifier_type = self.row_identifier_type.value

        public = self.public

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "name": name,
                "order": order,
                "type": type,
                "table": table,
                "public_view_has_password": public_view_has_password,
                "ownership_type": ownership_type,
                "slug": slug,
            }
        )
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sortings is not UNSET:
            field_dict["sortings"] = sortings
        if decorations is not UNSET:
            field_dict["decorations"] = decorations
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
        if show_logo is not UNSET:
            field_dict["show_logo"] = show_logo
        if row_identifier_type is not UNSET:
            field_dict["row_identifier_type"] = row_identifier_type
        if public is not UNSET:
            field_dict["public"] = public

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.table import Table
        from ..models.view_decoration import ViewDecoration
        from ..models.view_filter import ViewFilter
        from ..models.view_sort import ViewSort

        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        table = Table.from_dict(d.pop("table"))

        public_view_has_password = d.pop("public_view_has_password")

        ownership_type = d.pop("ownership_type")

        slug = d.pop("slug")

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = ViewFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        sortings = []
        _sortings = d.pop("sortings", UNSET)
        for sortings_item_data in _sortings or []:
            sortings_item = ViewSort.from_dict(sortings_item_data)

            sortings.append(sortings_item)

        decorations = []
        _decorations = d.pop("decorations", UNSET)
        for decorations_item_data in _decorations or []:
            decorations_item = ViewDecoration.from_dict(decorations_item_data)

            decorations.append(decorations_item)

        filters_disabled = d.pop("filters_disabled", UNSET)

        show_logo = d.pop("show_logo", UNSET)

        _row_identifier_type = d.pop("row_identifier_type", UNSET)
        row_identifier_type: Union[Unset, RowIdentifierTypeEnum]
        if isinstance(_row_identifier_type, Unset):
            row_identifier_type = UNSET
        else:
            row_identifier_type = RowIdentifierTypeEnum(_row_identifier_type)

        public = d.pop("public", UNSET)

        grid_view_view = cls(
            id=id,
            table_id=table_id,
            name=name,
            order=order,
            type=type,
            table=table,
            public_view_has_password=public_view_has_password,
            ownership_type=ownership_type,
            slug=slug,
            filter_type=filter_type,
            filters=filters,
            sortings=sortings,
            decorations=decorations,
            filters_disabled=filters_disabled,
            show_logo=show_logo,
            row_identifier_type=row_identifier_type,
            public=public,
        )

        grid_view_view.additional_properties = d
        return grid_view_view

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
