from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_database_table_grid_view_field_aggregations_response_200_field_id_type_3 import (
        GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3,
    )


T = TypeVar("T", bound="GetDatabaseTableGridViewFieldAggregationsResponse200")


@attr.s(auto_attribs=True)
class GetDatabaseTableGridViewFieldAggregationsResponse200:
    """
    Attributes:
        field_id (Union['GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3', List[Any], Unset, float,
            str]):
        total (Union[Unset, int]): The total value count. Only returned if `include=total` is specified as GET
            parameter. Example: 7.
    """

    field_id: Union[
        "GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3", List[Any], Unset, float, str
    ] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_database_table_grid_view_field_aggregations_response_200_field_id_type_3 import (
            GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3,
        )

        field_id: Union[Dict[str, Any], List[Any], Unset, float, str]
        if isinstance(self.field_id, Unset):
            field_id = UNSET

        elif isinstance(self.field_id, list):
            field_id = UNSET
            if not isinstance(self.field_id, Unset):
                field_id = self.field_id

        elif isinstance(self.field_id, GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3):
            field_id = UNSET
            if not isinstance(self.field_id, Unset):
                field_id = self.field_id.to_dict()

        else:
            field_id = self.field_id

        total = self.total

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_id is not UNSET:
            field_dict["field_{id}"] = field_id
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_database_table_grid_view_field_aggregations_response_200_field_id_type_3 import (
            GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3,
        )

        d = src_dict.copy()

        def _parse_field_id(
            data: object,
        ) -> Union["GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3", List[Any], Unset, float, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                field_id_type_2 = cast(List[Any], data)

                return field_id_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _field_id_type_3 = data
                field_id_type_3: Union[Unset, GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3]
                if isinstance(_field_id_type_3, Unset):
                    field_id_type_3 = UNSET
                else:
                    field_id_type_3 = GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3.from_dict(
                        _field_id_type_3
                    )

                return field_id_type_3
            except:  # noqa: E722
                pass
            return cast(
                Union["GetDatabaseTableGridViewFieldAggregationsResponse200FieldIdType3", List[Any], Unset, float, str],
                data,
            )

        field_id = _parse_field_id(d.pop("field_{id}", UNSET))

        total = d.pop("total", UNSET)

        get_database_table_grid_view_field_aggregations_response_200 = cls(
            field_id=field_id,
            total=total,
        )

        get_database_table_grid_view_field_aggregations_response_200.additional_properties = d
        return get_database_table_grid_view_field_aggregations_response_200

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
