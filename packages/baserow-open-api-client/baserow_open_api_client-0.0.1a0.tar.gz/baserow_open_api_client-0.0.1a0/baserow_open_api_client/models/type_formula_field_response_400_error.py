from enum import Enum


class TypeFormulaFieldResponse400Error(str, Enum):
    ERROR_FIELD_SELF_REFERENCE = "ERROR_FIELD_SELF_REFERENCE"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"
    ERROR_WITH_FORMULA = "ERROR_WITH_FORMULA"

    def __str__(self) -> str:
        return str(self.value)
