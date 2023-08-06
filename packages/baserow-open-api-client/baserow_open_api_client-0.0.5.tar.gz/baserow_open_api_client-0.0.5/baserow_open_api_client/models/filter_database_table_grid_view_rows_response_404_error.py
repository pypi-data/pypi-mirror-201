from enum import Enum


class FilterDatabaseTableGridViewRowsResponse404Error(str, Enum):
    ERROR_GRID_DOES_NOT_EXIST = "ERROR_GRID_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
