from enum import Enum


class LeaveWorkspaceResponse400Error(str, Enum):
    ERROR_GROUP_USER_IS_LAST_ADMIN = "ERROR_GROUP_USER_IS_LAST_ADMIN"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
