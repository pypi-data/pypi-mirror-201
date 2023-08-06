from enum import Enum


class UpdateDatabaseTableViewResponse400Error(str, Enum):
    ERROR_FIELD_NOT_IN_TABLE = "ERROR_FIELD_NOT_IN_TABLE"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
