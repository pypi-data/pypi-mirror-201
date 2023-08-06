from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_database_table_row_names_response_200_table_id import ListDatabaseTableRowNamesResponse200TableId


T = TypeVar("T", bound="ListDatabaseTableRowNamesResponse200")


@attr.s(auto_attribs=True)
class ListDatabaseTableRowNamesResponse200:
    """
    Attributes:
        table_id (Union[Unset, ListDatabaseTableRowNamesResponse200TableId]): An object containing the row names of
            table `table_id`.
    """

    table_id: Union[Unset, "ListDatabaseTableRowNamesResponse200TableId"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        table_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.table_id, Unset):
            table_id = self.table_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if table_id is not UNSET:
            field_dict["{table_id}*"] = table_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_database_table_row_names_response_200_table_id import (
            ListDatabaseTableRowNamesResponse200TableId,
        )

        d = src_dict.copy()
        _table_id = d.pop("{table_id}*", UNSET)
        table_id: Union[Unset, ListDatabaseTableRowNamesResponse200TableId]
        if isinstance(_table_id, Unset):
            table_id = UNSET
        else:
            table_id = ListDatabaseTableRowNamesResponse200TableId.from_dict(_table_id)

        list_database_table_row_names_response_200 = cls(
            table_id=table_id,
        )

        list_database_table_row_names_response_200.additional_properties = d
        return list_database_table_row_names_response_200

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
