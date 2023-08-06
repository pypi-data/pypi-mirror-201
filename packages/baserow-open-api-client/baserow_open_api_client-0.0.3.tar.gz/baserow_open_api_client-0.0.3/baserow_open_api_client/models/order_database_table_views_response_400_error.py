from enum import Enum


class OrderDatabaseTableViewsResponse400Error(str, Enum):
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"
    ERROR_VIEW_NOT_IN_TABLE = "ERROR_VIEW_NOT_IN_TABLE"

    def __str__(self) -> str:
        return str(self.value)
