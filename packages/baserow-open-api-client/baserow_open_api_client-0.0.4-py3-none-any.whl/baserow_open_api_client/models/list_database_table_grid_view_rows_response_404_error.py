from enum import Enum


class ListDatabaseTableGridViewRowsResponse404Error(str, Enum):
    ERROR_FIELD_DOES_NOT_EXIST = "ERROR_FIELD_DOES_NOT_EXIST"
    ERROR_GRID_DOES_NOT_EXIST = "ERROR_GRID_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
