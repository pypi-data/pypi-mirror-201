import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.file_field_response_thumbnails import FileFieldResponseThumbnails


T = TypeVar("T", bound="FileFieldResponse")


@attr.s(auto_attribs=True)
class FileFieldResponse:
    """
    Attributes:
        url (str):
        thumbnails (FileFieldResponseThumbnails):
        visible_name (str):
        name (str):
        size (int):
        mime_type (str):
        is_image (bool):
        image_width (int):
        image_height (int):
        uploaded_at (datetime.datetime):
    """

    url: str
    thumbnails: "FileFieldResponseThumbnails"
    visible_name: str
    name: str
    size: int
    mime_type: str
    is_image: bool
    image_width: int
    image_height: int
    uploaded_at: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        thumbnails = self.thumbnails.to_dict()

        visible_name = self.visible_name
        name = self.name
        size = self.size
        mime_type = self.mime_type
        is_image = self.is_image
        image_width = self.image_width
        image_height = self.image_height
        uploaded_at = self.uploaded_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "thumbnails": thumbnails,
                "visible_name": visible_name,
                "name": name,
                "size": size,
                "mime_type": mime_type,
                "is_image": is_image,
                "image_width": image_width,
                "image_height": image_height,
                "uploaded_at": uploaded_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_field_response_thumbnails import FileFieldResponseThumbnails

        d = src_dict.copy()
        url = d.pop("url")

        thumbnails = FileFieldResponseThumbnails.from_dict(d.pop("thumbnails"))

        visible_name = d.pop("visible_name")

        name = d.pop("name")

        size = d.pop("size")

        mime_type = d.pop("mime_type")

        is_image = d.pop("is_image")

        image_width = d.pop("image_width")

        image_height = d.pop("image_height")

        uploaded_at = isoparse(d.pop("uploaded_at"))

        file_field_response = cls(
            url=url,
            thumbnails=thumbnails,
            visible_name=visible_name,
            name=name,
            size=size,
            mime_type=mime_type,
            is_image=is_image,
            image_width=image_width,
            image_height=image_height,
            uploaded_at=uploaded_at,
        )

        file_field_response.additional_properties = d
        return file_field_response

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
