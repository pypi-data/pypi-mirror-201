from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.view_filter_preload_values import ViewFilterPreloadValues


T = TypeVar("T", bound="ViewFilter")


@attr.s(auto_attribs=True)
class ViewFilter:
    """
    Attributes:
        id (int):
        view (int): The view to which the filter applies. Each view can have his own filters.
        field (int): The field of which the value must be compared to the filter value.
        type (str): Indicates how the field's value must be compared to the filter's value. The filter is always in this
            order `field` `type` `value` (example: `field_1` `contains` `Test`).
        preload_values (ViewFilterPreloadValues): Can contain unique preloaded values per filter. This is for example
            used by the `link_row_has` filter to communicate the display name if a value is provided.
        value (Union[Unset, str]): The filter value that must be compared to the field's value.
    """

    id: int
    view: int
    field: int
    type: str
    preload_values: "ViewFilterPreloadValues"
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        view = self.view
        field = self.field
        type = self.type
        preload_values = self.preload_values.to_dict()

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "view": view,
                "field": field,
                "type": type,
                "preload_values": preload_values,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.view_filter_preload_values import ViewFilterPreloadValues

        d = src_dict.copy()
        id = d.pop("id")

        view = d.pop("view")

        field = d.pop("field")

        type = d.pop("type")

        preload_values = ViewFilterPreloadValues.from_dict(d.pop("preload_values"))

        value = d.pop("value", UNSET)

        view_filter = cls(
            id=id,
            view=view,
            field=field,
            type=type,
            preload_values=preload_values,
            value=value,
        )

        view_filter.additional_properties = d
        return view_filter

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
