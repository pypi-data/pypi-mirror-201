from enum import Enum


class UpdateBuilderPageElementResponse400Error(str, Enum):
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)
