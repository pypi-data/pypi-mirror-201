from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aggregation_raw_type_enum import AggregationRawTypeEnum
from ..models.blank_enum import BlankEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GridViewFieldOptions")


@attr.s(auto_attribs=True)
class GridViewFieldOptions:
    """
    Attributes:
        width (Union[Unset, int]): The width of the table field in the related view.
        hidden (Union[Unset, bool]): Whether or not the field should be hidden in the current view.
        order (Union[Unset, int]): The position that the field has within the view, lowest first. If there is another
            field with the same order value then the field with the lowest id must be shown first.
        aggregation_type (Union[Unset, str]): Indicates how the field value is aggregated. This value is different from
            the `aggregation_raw_type`. The `aggregation_raw_type` is the value extracted from the database, while the
            `aggregation_type` can implies further calculations. For example: if you want to compute an average, `sum` is
            going to be the `aggregation_raw_type`, the value extracted from database, and `sum / row_count` will be the
            aggregation result displayed to the user. This aggregation_type should be used by the client to compute the
            final value.
        aggregation_raw_type (Union[AggregationRawTypeEnum, BlankEnum, Unset]): Indicates how to compute the raw
            aggregation value from database. This type must be registered in the backend prior to use it.
    """

    width: Union[Unset, int] = UNSET
    hidden: Union[Unset, bool] = UNSET
    order: Union[Unset, int] = UNSET
    aggregation_type: Union[Unset, str] = UNSET
    aggregation_raw_type: Union[AggregationRawTypeEnum, BlankEnum, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        width = self.width
        hidden = self.hidden
        order = self.order
        aggregation_type = self.aggregation_type
        aggregation_raw_type: Union[Unset, str]
        if isinstance(self.aggregation_raw_type, Unset):
            aggregation_raw_type = UNSET

        elif isinstance(self.aggregation_raw_type, AggregationRawTypeEnum):
            aggregation_raw_type = UNSET
            if not isinstance(self.aggregation_raw_type, Unset):
                aggregation_raw_type = self.aggregation_raw_type.value

        else:
            aggregation_raw_type = UNSET
            if not isinstance(self.aggregation_raw_type, Unset):
                aggregation_raw_type = self.aggregation_raw_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if width is not UNSET:
            field_dict["width"] = width
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if order is not UNSET:
            field_dict["order"] = order
        if aggregation_type is not UNSET:
            field_dict["aggregation_type"] = aggregation_type
        if aggregation_raw_type is not UNSET:
            field_dict["aggregation_raw_type"] = aggregation_raw_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        width = d.pop("width", UNSET)

        hidden = d.pop("hidden", UNSET)

        order = d.pop("order", UNSET)

        aggregation_type = d.pop("aggregation_type", UNSET)

        def _parse_aggregation_raw_type(data: object) -> Union[AggregationRawTypeEnum, BlankEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _aggregation_raw_type_type_0 = data
                aggregation_raw_type_type_0: Union[Unset, AggregationRawTypeEnum]
                if isinstance(_aggregation_raw_type_type_0, Unset):
                    aggregation_raw_type_type_0 = UNSET
                else:
                    aggregation_raw_type_type_0 = AggregationRawTypeEnum(_aggregation_raw_type_type_0)

                return aggregation_raw_type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            _aggregation_raw_type_type_1 = data
            aggregation_raw_type_type_1: Union[Unset, BlankEnum]
            if isinstance(_aggregation_raw_type_type_1, Unset):
                aggregation_raw_type_type_1 = UNSET
            else:
                aggregation_raw_type_type_1 = BlankEnum(_aggregation_raw_type_type_1)

            return aggregation_raw_type_type_1

        aggregation_raw_type = _parse_aggregation_raw_type(d.pop("aggregation_raw_type", UNSET))

        grid_view_field_options = cls(
            width=width,
            hidden=hidden,
            order=order,
            aggregation_type=aggregation_type,
            aggregation_raw_type=aggregation_raw_type,
        )

        grid_view_field_options.additional_properties = d
        return grid_view_field_options

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
