from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_database_table_grid_view_field_aggregation_response_200_value_type_3 import (
        GetDatabaseTableGridViewFieldAggregationResponse200ValueType3,
    )


T = TypeVar("T", bound="GetDatabaseTableGridViewFieldAggregationResponse200")


@attr.s(auto_attribs=True)
class GetDatabaseTableGridViewFieldAggregationResponse200:
    """
    Attributes:
        value (Union['GetDatabaseTableGridViewFieldAggregationResponse200ValueType3', List[Any], float, str]):
        total (Union[Unset, int]): The total value count. Only returned if `include=total` is specified as GET
            parameter. Example: 7.
    """

    value: Union["GetDatabaseTableGridViewFieldAggregationResponse200ValueType3", List[Any], float, str]
    total: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_database_table_grid_view_field_aggregation_response_200_value_type_3 import (
            GetDatabaseTableGridViewFieldAggregationResponse200ValueType3,
        )

        value: Union[Dict[str, Any], List[Any], float, str]

        if isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, GetDatabaseTableGridViewFieldAggregationResponse200ValueType3):
            value = self.value.to_dict()

        else:
            value = self.value

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_database_table_grid_view_field_aggregation_response_200_value_type_3 import (
            GetDatabaseTableGridViewFieldAggregationResponse200ValueType3,
        )

        d = src_dict.copy()

        def _parse_value(
            data: object,
        ) -> Union["GetDatabaseTableGridViewFieldAggregationResponse200ValueType3", List[Any], float, str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_2 = cast(List[Any], data)

                return value_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_3 = GetDatabaseTableGridViewFieldAggregationResponse200ValueType3.from_dict(data)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(
                Union["GetDatabaseTableGridViewFieldAggregationResponse200ValueType3", List[Any], float, str], data
            )

        value = _parse_value(d.pop("value"))

        total = d.pop("total", UNSET)

        get_database_table_grid_view_field_aggregation_response_200 = cls(
            value=value,
            total=total,
        )

        get_database_table_grid_view_field_aggregation_response_200.additional_properties = d
        return get_database_table_grid_view_field_aggregation_response_200

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
