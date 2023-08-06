from enum import Enum


class BatchDeleteDatabaseTableRowsResponse404Error(str, Enum):
    ERROR_ROW_DOES_NOT_EXIST = "ERROR_ROW_DOES_NOT_EXIST"
    ERROR_TABLE_DOES_NOT_EXIST = "ERROR_TABLE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
