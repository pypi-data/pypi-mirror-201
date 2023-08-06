from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..models.mode_enum import ModeEnum
from ..models.submit_action_enum import SubmitActionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.table import Table
    from ..models.user_file import UserFile
    from ..models.view_decoration import ViewDecoration
    from ..models.view_filter import ViewFilter
    from ..models.view_sort import ViewSort


T = TypeVar("T", bound="FormViewView")


@attr.s(auto_attribs=True)
class FormViewView:
    """
    Attributes:
        id (int):
        table_id (int):
        name (str):
        order (int):
        type (str):
        table (Table):
        public_view_has_password (bool):
        ownership_type (str):
        slug (str): The unique slug that can be used to construct a public URL.
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters (Union[Unset, List['ViewFilter']]):
        sortings (Union[Unset, List['ViewSort']]):
        decorations (Union[Unset, List['ViewDecoration']]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
        show_logo (Union[Unset, bool]):
        title (Union[Unset, str]): The title that is displayed at the beginning of the form.
        description (Union[Unset, str]): The description that is displayed at the beginning of the form.
        mode (Union[Unset, ModeEnum]):
        cover_image (Union[Unset, None, UserFile]):
        logo_image (Union[Unset, None, UserFile]):
        submit_text (Union[Unset, str]): The text displayed on the submit button.
        submit_action (Union[Unset, SubmitActionEnum]):
        submit_action_message (Union[Unset, str]): If the `submit_action` is MESSAGE, then this message will be shown to
            the visitor after submitting the form.
        submit_action_redirect_url (Union[Unset, str]): If the `submit_action` is REDIRECT,then the visitors will be
            redirected to the this URL after submitting the form.
        public (Union[Unset, bool]): Indicates whether the view is publicly accessible to visitors.
    """

    id: int
    table_id: int
    name: str
    order: int
    type: str
    table: "Table"
    public_view_has_password: bool
    ownership_type: str
    slug: str
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters: Union[Unset, List["ViewFilter"]] = UNSET
    sortings: Union[Unset, List["ViewSort"]] = UNSET
    decorations: Union[Unset, List["ViewDecoration"]] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
    show_logo: Union[Unset, bool] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    mode: Union[Unset, ModeEnum] = UNSET
    cover_image: Union[Unset, None, "UserFile"] = UNSET
    logo_image: Union[Unset, None, "UserFile"] = UNSET
    submit_text: Union[Unset, str] = UNSET
    submit_action: Union[Unset, SubmitActionEnum] = UNSET
    submit_action_message: Union[Unset, str] = UNSET
    submit_action_redirect_url: Union[Unset, str] = UNSET
    public: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        table_id = self.table_id
        name = self.name
        order = self.order
        type = self.type
        table = self.table.to_dict()

        public_view_has_password = self.public_view_has_password
        ownership_type = self.ownership_type
        slug = self.slug
        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        sortings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sortings, Unset):
            sortings = []
            for sortings_item_data in self.sortings:
                sortings_item = sortings_item_data.to_dict()

                sortings.append(sortings_item)

        decorations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.decorations, Unset):
            decorations = []
            for decorations_item_data in self.decorations:
                decorations_item = decorations_item_data.to_dict()

                decorations.append(decorations_item)

        filters_disabled = self.filters_disabled
        show_logo = self.show_logo
        title = self.title
        description = self.description
        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        cover_image: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.cover_image, Unset):
            cover_image = self.cover_image.to_dict() if self.cover_image else None

        logo_image: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.logo_image, Unset):
            logo_image = self.logo_image.to_dict() if self.logo_image else None

        submit_text = self.submit_text
        submit_action: Union[Unset, str] = UNSET
        if not isinstance(self.submit_action, Unset):
            submit_action = self.submit_action.value

        submit_action_message = self.submit_action_message
        submit_action_redirect_url = self.submit_action_redirect_url
        public = self.public

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "table_id": table_id,
                "name": name,
                "order": order,
                "type": type,
                "table": table,
                "public_view_has_password": public_view_has_password,
                "ownership_type": ownership_type,
                "slug": slug,
            }
        )
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sortings is not UNSET:
            field_dict["sortings"] = sortings
        if decorations is not UNSET:
            field_dict["decorations"] = decorations
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
        if show_logo is not UNSET:
            field_dict["show_logo"] = show_logo
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if mode is not UNSET:
            field_dict["mode"] = mode
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if logo_image is not UNSET:
            field_dict["logo_image"] = logo_image
        if submit_text is not UNSET:
            field_dict["submit_text"] = submit_text
        if submit_action is not UNSET:
            field_dict["submit_action"] = submit_action
        if submit_action_message is not UNSET:
            field_dict["submit_action_message"] = submit_action_message
        if submit_action_redirect_url is not UNSET:
            field_dict["submit_action_redirect_url"] = submit_action_redirect_url
        if public is not UNSET:
            field_dict["public"] = public

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.table import Table
        from ..models.user_file import UserFile
        from ..models.view_decoration import ViewDecoration
        from ..models.view_filter import ViewFilter
        from ..models.view_sort import ViewSort

        d = src_dict.copy()
        id = d.pop("id")

        table_id = d.pop("table_id")

        name = d.pop("name")

        order = d.pop("order")

        type = d.pop("type")

        table = Table.from_dict(d.pop("table"))

        public_view_has_password = d.pop("public_view_has_password")

        ownership_type = d.pop("ownership_type")

        slug = d.pop("slug")

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = ViewFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        sortings = []
        _sortings = d.pop("sortings", UNSET)
        for sortings_item_data in _sortings or []:
            sortings_item = ViewSort.from_dict(sortings_item_data)

            sortings.append(sortings_item)

        decorations = []
        _decorations = d.pop("decorations", UNSET)
        for decorations_item_data in _decorations or []:
            decorations_item = ViewDecoration.from_dict(decorations_item_data)

            decorations.append(decorations_item)

        filters_disabled = d.pop("filters_disabled", UNSET)

        show_logo = d.pop("show_logo", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, ModeEnum]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = ModeEnum(_mode)

        _cover_image = d.pop("cover_image", UNSET)
        cover_image: Union[Unset, None, UserFile]
        if _cover_image is None:
            cover_image = None
        elif isinstance(_cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = UserFile.from_dict(_cover_image)

        _logo_image = d.pop("logo_image", UNSET)
        logo_image: Union[Unset, None, UserFile]
        if _logo_image is None:
            logo_image = None
        elif isinstance(_logo_image, Unset):
            logo_image = UNSET
        else:
            logo_image = UserFile.from_dict(_logo_image)

        submit_text = d.pop("submit_text", UNSET)

        _submit_action = d.pop("submit_action", UNSET)
        submit_action: Union[Unset, SubmitActionEnum]
        if isinstance(_submit_action, Unset):
            submit_action = UNSET
        else:
            submit_action = SubmitActionEnum(_submit_action)

        submit_action_message = d.pop("submit_action_message", UNSET)

        submit_action_redirect_url = d.pop("submit_action_redirect_url", UNSET)

        public = d.pop("public", UNSET)

        form_view_view = cls(
            id=id,
            table_id=table_id,
            name=name,
            order=order,
            type=type,
            table=table,
            public_view_has_password=public_view_has_password,
            ownership_type=ownership_type,
            slug=slug,
            filter_type=filter_type,
            filters=filters,
            sortings=sortings,
            decorations=decorations,
            filters_disabled=filters_disabled,
            show_logo=show_logo,
            title=title,
            description=description,
            mode=mode,
            cover_image=cover_image,
            logo_image=logo_image,
            submit_text=submit_text,
            submit_action=submit_action,
            submit_action_message=submit_action_message,
            submit_action_redirect_url=submit_action_redirect_url,
            public=public,
        )

        form_view_view.additional_properties = d
        return form_view_view

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
