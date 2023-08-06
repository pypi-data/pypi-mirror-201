from enum import Enum


class UpdateWorkspaceUserResponse400Error(str, Enum):
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_INVALID_GROUP_PERMISSIONS = "ERROR_USER_INVALID_GROUP_PERMISSIONS"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
