from enum import Enum


class DuplicateDatabaseTableViewResponse404Error(str, Enum):
    ERROR_VIEW_DOES_NOT_EXIST = "ERROR_VIEW_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
