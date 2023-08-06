import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RowComment")


@attr.s(auto_attribs=True)
class RowComment:
    """
    Attributes:
        id (int):
        table_id (int): The table the row this comment is for is found in.
        row_id (int): The id of the row the comment is for.
        comment (str): The users comment.
        created_on (datetime.datetime):
        updated_on (datetime.datetime):
        first_name (Union[Unset, str]):
        user_id (Optional[int]): The user who made the comment.
    """

    id: int
    table_id: int
    row_id: int
    comment: str
    created_on: datetime.datetime
    updated_on: datetime.datetime
    user_id: Optional[int]
    first_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        row_id = self.row_id
        comment = self.comment
        created_on = self.created_on.isoformat()

        updated_on = self.updated_on.isoformat()

        first_name = self.first_name
        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "row_id": row_id,
                "comment": comment,
                "created_on": created_on,
                "updated_on": updated_on,
                "user_id": user_id,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        row_id = d.pop("row_id")

        comment = d.pop("comment")

        created_on = isoparse(d.pop("created_on"))

        updated_on = isoparse(d.pop("updated_on"))

        first_name = d.pop("first_name", UNSET)

        user_id = d.pop("user_id")

        row_comment = cls(
            id=id,
            table_id=table_id,
            row_id=row_id,
            comment=comment,
            created_on=created_on,
            updated_on=updated_on,
            first_name=first_name,
            user_id=user_id,
        )

        row_comment.additional_properties = d
        return row_comment

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
