from enum import Enum


class ListRoleAssignmentsResponse404Error(str, Enum):
    ERROR_GROUP_DOES_NOT_EXIST = "ERROR_GROUP_DOES_NOT_EXIST"
    ERROR_OBJECT_SCOPE_TYPE_DOES_NOT_EXIST = "ERROR_OBJECT_SCOPE_TYPE_DOES_NOT_EXIST"
    ERROR_SCOPE_DOES_NOT_EXIST = "ERROR_SCOPE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
