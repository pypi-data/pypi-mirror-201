import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_file_thumbnails import UserFileThumbnails


T = TypeVar("T", bound="UserFile")


@attr.s(auto_attribs=True)
class UserFile:
    """
    Attributes:
        size (int):
        uploaded_at (datetime.datetime):
        url (str):
        thumbnails (UserFileThumbnails):
        name (str):
        original_name (str):
        mime_type (Union[Unset, str]):
        is_image (Union[Unset, bool]):
        image_width (Union[Unset, None, int]):
        image_height (Union[Unset, None, int]):
    """

    size: int
    uploaded_at: datetime.datetime
    url: str
    thumbnails: "UserFileThumbnails"
    name: str
    original_name: str
    mime_type: Union[Unset, str] = UNSET
    is_image: Union[Unset, bool] = UNSET
    image_width: Union[Unset, None, int] = UNSET
    image_height: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        uploaded_at = self.uploaded_at.isoformat()

        url = self.url
        thumbnails = self.thumbnails.to_dict()

        name = self.name
        original_name = self.original_name
        mime_type = self.mime_type
        is_image = self.is_image
        image_width = self.image_width
        image_height = self.image_height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "size": size,
                "uploaded_at": uploaded_at,
                "url": url,
                "thumbnails": thumbnails,
                "name": name,
                "original_name": original_name,
            }
        )
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type
        if is_image is not UNSET:
            field_dict["is_image"] = is_image
        if image_width is not UNSET:
            field_dict["image_width"] = image_width
        if image_height is not UNSET:
            field_dict["image_height"] = image_height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_file_thumbnails import UserFileThumbnails

        d = src_dict.copy()
        size = d.pop("size")

        uploaded_at = isoparse(d.pop("uploaded_at"))

        url = d.pop("url")

        thumbnails = UserFileThumbnails.from_dict(d.pop("thumbnails"))

        name = d.pop("name")

        original_name = d.pop("original_name")

        mime_type = d.pop("mime_type", UNSET)

        is_image = d.pop("is_image", UNSET)

        image_width = d.pop("image_width", UNSET)

        image_height = d.pop("image_height", UNSET)

        user_file = cls(
            size=size,
            uploaded_at=uploaded_at,
            url=url,
            thumbnails=thumbnails,
            name=name,
            original_name=original_name,
            mime_type=mime_type,
            is_image=is_image,
            image_width=image_width,
            image_height=image_height,
        )

        user_file.additional_properties = d
        return user_file

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
