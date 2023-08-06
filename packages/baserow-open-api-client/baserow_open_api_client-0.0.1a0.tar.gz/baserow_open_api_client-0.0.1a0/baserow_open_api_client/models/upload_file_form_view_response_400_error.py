from enum import Enum


class UploadFileFormViewResponse400Error(str, Enum):
    ERROR_FILE_SIZE_TOO_LARGE = "ERROR_FILE_SIZE_TOO_LARGE"
    ERROR_INVALID_FILE = "ERROR_INVALID_FILE"
    ERROR_VIEW_HAS_NO_PUBLIC_FILE_FIELD = "ERROR_VIEW_HAS_NO_PUBLIC_FILE_FIELD"

    def __str__(self) -> str:
        return str(self.value)
