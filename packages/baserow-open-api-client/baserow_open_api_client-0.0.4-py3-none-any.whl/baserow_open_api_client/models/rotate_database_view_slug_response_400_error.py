from enum import Enum


class RotateDatabaseViewSlugResponse400Error(str, Enum):
    ERROR_CANNOT_SHARE_VIEW_TYPE = "ERROR_CANNOT_SHARE_VIEW_TYPE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
