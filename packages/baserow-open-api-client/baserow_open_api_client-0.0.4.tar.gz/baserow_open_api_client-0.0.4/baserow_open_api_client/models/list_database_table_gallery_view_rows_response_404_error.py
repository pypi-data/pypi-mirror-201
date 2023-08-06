from enum import Enum


class ListDatabaseTableGalleryViewRowsResponse404Error(str, Enum):
    ERROR_GALLERY_DOES_NOT_EXIST = "ERROR_GALLERY_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
