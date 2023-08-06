from enum import Enum


class GetDatabaseTableViewSortResponse404Error(str, Enum):
    ERROR_VIEW_SORT_DOES_NOT_EXIST = "ERROR_VIEW_SORT_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
