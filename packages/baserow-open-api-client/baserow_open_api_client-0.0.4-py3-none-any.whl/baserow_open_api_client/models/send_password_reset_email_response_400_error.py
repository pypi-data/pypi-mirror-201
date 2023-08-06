from enum import Enum


class SendPasswordResetEmailResponse400Error(str, Enum):
    ERROR_HOSTNAME_IS_NOT_ALLOWED = "ERROR_HOSTNAME_IS_NOT_ALLOWED"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)
