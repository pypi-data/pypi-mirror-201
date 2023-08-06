from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TableCreate")


@attr.s(auto_attribs=True)
class TableCreate:
    """
    Attributes:
        name (str):
        data (Union[Unset, List[Any]]): A list of rows that needs to be created as initial table data. Each row is a
            list of values that are going to be added in the new table in the same order as provided.

            Ex:
            ```json
            [
              ["row1_field1_value", "row1_field2_value"],
              ["row2_field1_value", "row2_field2_value"],
            ]
            ```
            for creating a two rows table with two fields.

            If not provided, some example data is going to be created.
        first_row_header (Union[Unset, bool]): Indicates if the first provided row is the header. If true the field
            names are going to be the values of the first row. Otherwise they will be called "Field N"
    """

    name: str
    data: Union[Unset, List[Any]] = UNSET
    first_row_header: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        data: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data

        first_row_header = self.first_row_header

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data
        if first_row_header is not UNSET:
            field_dict["first_row_header"] = first_row_header

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        data = cast(List[Any], d.pop("data", UNSET))

        first_row_header = d.pop("first_row_header", UNSET)

        table_create = cls(
            name=name,
            data=data,
            first_row_header=first_row_header,
        )

        table_create.additional_properties = d
        return table_create

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
