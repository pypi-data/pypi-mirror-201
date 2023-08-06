from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="TableImport")


@attr.s(auto_attribs=True)
class TableImport:
    """
    Attributes:
        data (List[Any]): A list of rows you want to add to the specified table. Each row is a list of values, one for
            each **writable** field. The field values must be ordered according to the field order in the table. All values
            must be compatible with the corresponding field type.

            Ex:
            ```json
            [
              ["row1_field1_value", "row1_field2_value"],
              ["row2_field1_value", "row2_field2_value"],
            ]
            ```
            for adding two rows to a table with two writable fields.
    """

    data: List[Any]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = cast(List[Any], d.pop("data"))

        table_import = cls(
            data=data,
        )

        table_import.additional_properties = d
        return table_import

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
