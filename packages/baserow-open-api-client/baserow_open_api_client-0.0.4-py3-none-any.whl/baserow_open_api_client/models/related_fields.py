from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.field import Field


T = TypeVar("T", bound="RelatedFields")


@attr.s(auto_attribs=True)
class RelatedFields:
    """
    Attributes:
        related_fields (List['Field']): A list of related fields which also changed.
    """

    related_fields: List["Field"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        related_fields = []
        for related_fields_item_data in self.related_fields:
            related_fields_item = related_fields_item_data.to_dict()

            related_fields.append(related_fields_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "related_fields": related_fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field import Field

        d = src_dict.copy()
        related_fields = []
        _related_fields = d.pop("related_fields")
        for related_fields_item_data in _related_fields:
            related_fields_item = Field.from_dict(related_fields_item_data)

            related_fields.append(related_fields_item)

        related_fields = cls(
            related_fields=related_fields,
        )

        related_fields.additional_properties = d
        return related_fields

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
