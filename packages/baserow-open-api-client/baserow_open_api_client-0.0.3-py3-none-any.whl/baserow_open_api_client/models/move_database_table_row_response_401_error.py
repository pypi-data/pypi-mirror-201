from enum import Enum


class MoveDatabaseTableRowResponse401Error(str, Enum):
    ERROR_NO_PERMISSION_TO_TABLE = "ERROR_NO_PERMISSION_TO_TABLE"

    def __str__(self) -> str:
        return str(self.value)
