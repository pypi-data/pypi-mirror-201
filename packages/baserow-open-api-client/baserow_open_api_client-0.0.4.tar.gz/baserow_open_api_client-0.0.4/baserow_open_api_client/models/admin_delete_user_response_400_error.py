from enum import Enum


class AdminDeleteUserResponse400Error(str, Enum):
    ERROR_FEATURE_NOT_AVAILABLE = "ERROR_FEATURE_NOT_AVAILABLE"
    USER_ADMIN_CANNOT_DELETE_SELF = "USER_ADMIN_CANNOT_DELETE_SELF"
    USER_ADMIN_UNKNOWN_USER = "USER_ADMIN_UNKNOWN_USER"

    def __str__(self) -> str:
        return str(self.value)
