from enum import Enum


class SubmitDatabaseTableFormViewResponse401Error(str, Enum):
    ERROR_NO_PERMISSION_TO_PUBLICLY_SHARED_FORM = "ERROR_NO_PERMISSION_TO_PUBLICLY_SHARED_FORM"

    def __str__(self) -> str:
        return str(self.value)
