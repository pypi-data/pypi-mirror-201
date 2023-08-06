from enum import Enum


class AssignRoleResponse400Error(str, Enum):
    ERROR_CANT_ASSIGN_ROLE_EXCEPTION_TO_ADMIN = "ERROR_CANT_ASSIGN_ROLE_EXCEPTION_TO_ADMIN"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
