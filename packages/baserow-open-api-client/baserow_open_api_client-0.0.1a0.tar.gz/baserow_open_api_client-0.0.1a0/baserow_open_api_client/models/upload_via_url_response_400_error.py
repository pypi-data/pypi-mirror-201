from enum import Enum


class UploadViaUrlResponse400Error(str, Enum):
    ERROR_FILE_SIZE_TOO_LARGE = "ERROR_FILE_SIZE_TOO_LARGE"
    ERROR_FILE_URL_COULD_NOT_BE_REACHED = "ERROR_FILE_URL_COULD_NOT_BE_REACHED"
    ERROR_INVALID_FILE = "ERROR_INVALID_FILE"
    ERROR_INVALID_FILE_URL = "ERROR_INVALID_FILE_URL"

    def __str__(self) -> str:
        return str(self.value)
