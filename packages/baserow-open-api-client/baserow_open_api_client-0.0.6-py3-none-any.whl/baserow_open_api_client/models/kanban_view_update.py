from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="KanbanViewUpdate")


@attr.s(auto_attribs=True)
class KanbanViewUpdate:
    """
    Attributes:
        slug (str): The unique slug that can be used to construct a public URL.
        name (Union[Unset, str]):
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
        public_view_password (Union[Unset, str]): The password required to access the public view URL.
        single_select_field (Union[Unset, None, int]):
        card_cover_image_field (Union[Unset, None, int]): References a file field of which the first image must be shown
            as card cover image.
        public (Union[Unset, bool]): Indicates whether the view is publicly accessible to visitors.
    """

    slug: str
    name: Union[Unset, str] = UNSET
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
    public_view_password: Union[Unset, str] = UNSET
    single_select_field: Union[Unset, None, int] = UNSET
    card_cover_image_field: Union[Unset, None, int] = UNSET
    public: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slug = self.slug
        name = self.name
        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters_disabled = self.filters_disabled
        public_view_password = self.public_view_password
        single_select_field = self.single_select_field
        card_cover_image_field = self.card_cover_image_field
        public = self.public

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slug": slug,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
        if public_view_password is not UNSET:
            field_dict["public_view_password"] = public_view_password
        if single_select_field is not UNSET:
            field_dict["single_select_field"] = single_select_field
        if card_cover_image_field is not UNSET:
            field_dict["card_cover_image_field"] = card_cover_image_field
        if public is not UNSET:
            field_dict["public"] = public

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slug = d.pop("slug")

        name = d.pop("name", UNSET)

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters_disabled = d.pop("filters_disabled", UNSET)

        public_view_password = d.pop("public_view_password", UNSET)

        single_select_field = d.pop("single_select_field", UNSET)

        card_cover_image_field = d.pop("card_cover_image_field", UNSET)

        public = d.pop("public", UNSET)

        kanban_view_update = cls(
            slug=slug,
            name=name,
            filter_type=filter_type,
            filters_disabled=filters_disabled,
            public_view_password=public_view_password,
            single_select_field=single_select_field,
            card_cover_image_field=card_cover_image_field,
            public=public,
        )

        kanban_view_update.additional_properties = d
        return kanban_view_update

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
