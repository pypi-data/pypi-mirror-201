from enum import Enum


class GetDatabaseTableFieldResponse404Error(str, Enum):
    ERROR_FIELD_DOES_NOT_EXIST = "ERROR_FIELD_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
