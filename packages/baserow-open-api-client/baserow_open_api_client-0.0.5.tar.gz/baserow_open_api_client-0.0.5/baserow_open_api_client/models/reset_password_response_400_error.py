from enum import Enum


class ResetPasswordResponse400Error(str, Enum):
    BAD_TOKEN_SIGNATURE = "BAD_TOKEN_SIGNATURE"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_FOUND = "ERROR_USER_NOT_FOUND"
    EXPIRED_TOKEN_SIGNATURE = "EXPIRED_TOKEN_SIGNATURE"

    def __str__(self) -> str:
        return str(self.value)
