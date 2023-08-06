from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.view_decoration_value_provider_conf import ViewDecorationValueProviderConf


T = TypeVar("T", bound="ViewDecoration")


@attr.s(auto_attribs=True)
class ViewDecoration:
    """
    Attributes:
        id (int):
        view (Union[Unset, int]): The view to which the decoration applies. Each view can have his own decorations.
        type (Union[Unset, str]): The decorator type. This is then interpreted by the frontend to display the
            decoration.
        value_provider_type (Union[Unset, str]): The value provider type that gives the value to the decorator.
        value_provider_conf (Union[Unset, ViewDecorationValueProviderConf]): The configuration consumed by the value
            provider.
        order (Union[Unset, int]): The position of the decorator has within the view, lowest first. If there is another
            decorator with the same order value then the decorator with the lowest id must be shown first.
    """

    id: int
    view: Union[Unset, int] = UNSET
    type: Union[Unset, str] = UNSET
    value_provider_type: Union[Unset, str] = UNSET
    value_provider_conf: Union[Unset, "ViewDecorationValueProviderConf"] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        view = self.view
        type = self.type
        value_provider_type = self.value_provider_type
        value_provider_conf: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.value_provider_conf, Unset):
            value_provider_conf = self.value_provider_conf.to_dict()

        order = self.order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if view is not UNSET:
            field_dict["view"] = view
        if type is not UNSET:
            field_dict["type"] = type
        if value_provider_type is not UNSET:
            field_dict["value_provider_type"] = value_provider_type
        if value_provider_conf is not UNSET:
            field_dict["value_provider_conf"] = value_provider_conf
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.view_decoration_value_provider_conf import ViewDecorationValueProviderConf

        d = src_dict.copy()
        id = d.pop("id")

        view = d.pop("view", UNSET)

        type = d.pop("type", UNSET)

        value_provider_type = d.pop("value_provider_type", UNSET)

        _value_provider_conf = d.pop("value_provider_conf", UNSET)
        value_provider_conf: Union[Unset, ViewDecorationValueProviderConf]
        if isinstance(_value_provider_conf, Unset):
            value_provider_conf = UNSET
        else:
            value_provider_conf = ViewDecorationValueProviderConf.from_dict(_value_provider_conf)

        order = d.pop("order", UNSET)

        view_decoration = cls(
            id=id,
            view=view,
            type=type,
            value_provider_type=value_provider_type,
            value_provider_conf=value_provider_conf,
            order=order,
        )

        view_decoration.additional_properties = d
        return view_decoration

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
