from enum import Enum


class UploadFileResponse400Error(str, Enum):
    ERROR_FILE_SIZE_TOO_LARGE = "ERROR_FILE_SIZE_TOO_LARGE"
    ERROR_INVALID_FILE = "ERROR_INVALID_FILE"

    def __str__(self) -> str:
        return str(self.value)
