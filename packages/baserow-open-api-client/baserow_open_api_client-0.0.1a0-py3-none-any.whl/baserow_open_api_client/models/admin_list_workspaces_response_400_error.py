from enum import Enum


class AdminListWorkspacesResponse400Error(str, Enum):
    ERROR_INVALID_PAGE = "ERROR_INVALID_PAGE"
    ERROR_INVALID_SORT_ATTRIBUTE = "ERROR_INVALID_SORT_ATTRIBUTE"
    ERROR_INVALID_SORT_DIRECTION = "ERROR_INVALID_SORT_DIRECTION"
    ERROR_PAGE_SIZE_LIMIT = "ERROR_PAGE_SIZE_LIMIT"

    def __str__(self) -> str:
        return str(self.value)
