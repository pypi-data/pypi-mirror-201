from enum import Enum


class ChangePasswordResponse400Error(str, Enum):
    ERROR_INVALID_OLD_PASSWORD = "ERROR_INVALID_OLD_PASSWORD"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)
