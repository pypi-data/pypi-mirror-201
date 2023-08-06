from enum import Enum


class SubmitDatabaseTableFormViewResponse404Error(str, Enum):
    ERROR_FORM_DOES_NOT_EXIST = "ERROR_FORM_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
