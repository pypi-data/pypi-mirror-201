from enum import Enum


class BatchDeleteDatabaseTableRowsResponse400Error(str, Enum):
    ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM = "ERROR_CANNOT_DELETE_ALREADY_DELETED_ITEM"
    ERROR_ROW_IDS_NOT_UNIQUE = "ERROR_ROW_IDS_NOT_UNIQUE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
