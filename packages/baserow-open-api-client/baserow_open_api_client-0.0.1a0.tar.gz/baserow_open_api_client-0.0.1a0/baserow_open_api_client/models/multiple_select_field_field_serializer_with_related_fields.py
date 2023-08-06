from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field import Field
    from ..models.select_option import SelectOption


T = TypeVar("T", bound="MultipleSelectFieldFieldSerializerWithRelatedFields")


@attr.s(auto_attribs=True)
class MultipleSelectFieldFieldSerializerWithRelatedFields:
    """
    Attributes:
        id (int):
        table_id (int):
        name (str):
        order (int): Lowest first.
        type (str): The type of the related field.
        read_only (bool): Indicates whether the field is a read only field. If true, it's not possible to update the
            cell value.
        related_fields (List['Field']): A list of related fields which also changed.
        primary (Union[Unset, bool]): Indicates if the field is a primary field. If `true` the field cannot be deleted
            and the value should represent the whole row.
        select_options (Union[Unset, List['SelectOption']]):
    """

    id: int
    table_id: int
    name: str
    order: int
    type: str
    read_only: bool
    related_fields: List["Field"]
    primary: Union[Unset, bool] = UNSET
    select_options: Union[Unset, List["SelectOption"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        name = self.name
        order = self.order
        type = self.type
        read_only = self.read_only
        related_fields = []
        for related_fields_item_data in self.related_fields:
            related_fields_item = related_fields_item_data.to_dict()

            related_fields.append(related_fields_item)

        primary = self.primary
        select_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.select_options, Unset):
            select_options = []
            for select_options_item_data in self.select_options:
                select_options_item = select_options_item_data.to_dict()

                select_options.append(select_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "name": name,
                "order": order,
                "type": type,
                "read_only": read_only,
                "related_fields": related_fields,
            }
        )
        if primary is not UNSET:
            field_dict["primary"] = primary
        if select_options is not UNSET:
            field_dict["select_options"] = select_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field import Field
        from ..models.select_option import SelectOption

        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        read_only = d.pop("read_only")

        related_fields = []
        _related_fields = d.pop("related_fields")
        for related_fields_item_data in _related_fields:
            related_fields_item = Field.from_dict(related_fields_item_data)

            related_fields.append(related_fields_item)

        primary = d.pop("primary", UNSET)

        select_options = []
        _select_options = d.pop("select_options", UNSET)
        for select_options_item_data in _select_options or []:
            select_options_item = SelectOption.from_dict(select_options_item_data)

            select_options.append(select_options_item)

        multiple_select_field_field_serializer_with_related_fields = cls(
            id=id,
            table_id=table_id,
            name=name,
            order=order,
            type=type,
            read_only=read_only,
            related_fields=related_fields,
            primary=primary,
            select_options=select_options,
        )

        multiple_select_field_field_serializer_with_related_fields.additional_properties = d
        return multiple_select_field_field_serializer_with_related_fields

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
