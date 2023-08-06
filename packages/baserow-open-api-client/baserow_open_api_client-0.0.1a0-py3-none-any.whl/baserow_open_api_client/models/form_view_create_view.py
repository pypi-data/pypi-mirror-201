from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.condition_type_enum import ConditionTypeEnum
from ..models.mode_enum import ModeEnum
from ..models.ownership_type_enum import OwnershipTypeEnum
from ..models.submit_action_enum import SubmitActionEnum
from ..models.view_types_enum import ViewTypesEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_file import UserFile


T = TypeVar("T", bound="FormViewCreateView")


@attr.s(auto_attribs=True)
class FormViewCreateView:
    """
    Attributes:
        name (str):
        type (ViewTypesEnum):
        slug (str): The unique slug that can be used to construct a public URL.
        ownership_type (Union[Unset, OwnershipTypeEnum]):  Default: OwnershipTypeEnum.COLLABORATIVE.
        filter_type (Union[Unset, ConditionTypeEnum]):
        filters_disabled (Union[Unset, bool]): Allows users to see results unfiltered while still keeping the filters
            saved for the view.
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

    name: str
    type: ViewTypesEnum
    slug: str
    ownership_type: Union[Unset, OwnershipTypeEnum] = OwnershipTypeEnum.COLLABORATIVE
    filter_type: Union[Unset, ConditionTypeEnum] = UNSET
    filters_disabled: Union[Unset, bool] = UNSET
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
        name = self.name
        type = self.type.value

        slug = self.slug
        ownership_type: Union[Unset, str] = UNSET
        if not isinstance(self.ownership_type, Unset):
            ownership_type = self.ownership_type.value

        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        filters_disabled = self.filters_disabled
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
                "name": name,
                "type": type,
                "slug": slug,
            }
        )
        if ownership_type is not UNSET:
            field_dict["ownership_type"] = ownership_type
        if filter_type is not UNSET:
            field_dict["filter_type"] = filter_type
        if filters_disabled is not UNSET:
            field_dict["filters_disabled"] = filters_disabled
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
        from ..models.user_file import UserFile

        d = src_dict.copy()
        name = d.pop("name")

        type = ViewTypesEnum(d.pop("type"))

        slug = d.pop("slug")

        _ownership_type = d.pop("ownership_type", UNSET)
        ownership_type: Union[Unset, OwnershipTypeEnum]
        if isinstance(_ownership_type, Unset):
            ownership_type = UNSET
        else:
            ownership_type = OwnershipTypeEnum(_ownership_type)

        _filter_type = d.pop("filter_type", UNSET)
        filter_type: Union[Unset, ConditionTypeEnum]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = ConditionTypeEnum(_filter_type)

        filters_disabled = d.pop("filters_disabled", UNSET)

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

        form_view_create_view = cls(
            name=name,
            type=type,
            slug=slug,
            ownership_type=ownership_type,
            filter_type=filter_type,
            filters_disabled=filters_disabled,
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

        form_view_create_view.additional_properties = d
        return form_view_create_view

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
