from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListDatabaseTableRowNamesResponse200TableId")


@attr.s(auto_attribs=True)
class ListDatabaseTableRowNamesResponse200TableId:
    """An object containing the row names of table `table_id`.

    Attributes:
        row_id (Union[Unset, str]): the name of the row with id `row_id` from table with id `table_id`.
    """

    row_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_id = self.row_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if row_id is not UNSET:
            field_dict["{row_id}*"] = row_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        row_id = d.pop("{row_id}*", UNSET)

        list_database_table_row_names_response_200_table_id = cls(
            row_id=row_id,
        )

        list_database_table_row_names_response_200_table_id.additional_properties = d
        return list_database_table_row_names_response_200_table_id

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
