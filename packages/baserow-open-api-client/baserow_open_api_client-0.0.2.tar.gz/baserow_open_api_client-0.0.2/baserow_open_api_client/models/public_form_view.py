from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.mode_enum import ModeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.public_form_view_field_options import PublicFormViewFieldOptions
    from ..models.user_file import UserFile


T = TypeVar("T", bound="PublicFormView")


@attr.s(auto_attribs=True)
class PublicFormView:
    """
    Attributes:
        fields (List['PublicFormViewFieldOptions']):
        title (Union[Unset, str]): The title that is displayed at the beginning of the form.
        description (Union[Unset, str]): The description that is displayed at the beginning of the form.
        mode (Union[Unset, ModeEnum]):
        cover_image (Union[Unset, None, UserFile]):
        logo_image (Union[Unset, None, UserFile]):
        submit_text (Union[Unset, str]): The text displayed on the submit button.
        show_logo (Union[Unset, bool]):
    """

    fields: List["PublicFormViewFieldOptions"]
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    mode: Union[Unset, ModeEnum] = UNSET
    cover_image: Union[Unset, None, "UserFile"] = UNSET
    logo_image: Union[Unset, None, "UserFile"] = UNSET
    submit_text: Union[Unset, str] = UNSET
    show_logo: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()

            fields.append(fields_item)

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
        show_logo = self.show_logo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fields": fields,
            }
        )
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
        if show_logo is not UNSET:
            field_dict["show_logo"] = show_logo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.public_form_view_field_options import PublicFormViewFieldOptions
        from ..models.user_file import UserFile

        d = src_dict.copy()
        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = PublicFormViewFieldOptions.from_dict(fields_item_data)

            fields.append(fields_item)

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

        show_logo = d.pop("show_logo", UNSET)

        public_form_view = cls(
            fields=fields,
            title=title,
            description=description,
            mode=mode,
            cover_image=cover_image,
            logo_image=logo_image,
            submit_text=submit_text,
            show_logo=show_logo,
        )

        public_form_view.additional_properties = d
        return public_form_view

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
