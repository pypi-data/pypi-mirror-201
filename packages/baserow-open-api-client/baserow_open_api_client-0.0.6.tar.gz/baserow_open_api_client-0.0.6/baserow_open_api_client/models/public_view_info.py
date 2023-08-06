from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.public_field import PublicField
    from ..models.public_view import PublicView


T = TypeVar("T", bound="PublicViewInfo")


@attr.s(auto_attribs=True)
class PublicViewInfo:
    """
    Attributes:
        fields (List['PublicField']):
        view (PublicView):
    """

    fields: List["PublicField"]
    view: "PublicView"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()

            fields.append(fields_item)

        view = self.view.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fields": fields,
                "view": view,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.public_field import PublicField
        from ..models.public_view import PublicView

        d = src_dict.copy()
        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = PublicField.from_dict(fields_item_data)

            fields.append(fields_item)

        view = PublicView.from_dict(d.pop("view"))

        public_view_info = cls(
            fields=fields,
            view=view,
        )

        public_view_info.additional_properties = d
        return public_view_info

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
