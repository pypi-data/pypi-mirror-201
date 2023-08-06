from enum import Enum


class UpdateDatabaseTableViewSortResponse400Error(str, Enum):
    ERROR_FIELD_NOT_IN_TABLE = "ERROR_FIELD_NOT_IN_TABLE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"
    ERROR_VIEW_SORT_FIELD_ALREADY_EXISTS = "ERROR_VIEW_SORT_FIELD_ALREADY_EXISTS"

    def __str__(self) -> str:
        return str(self.value)
