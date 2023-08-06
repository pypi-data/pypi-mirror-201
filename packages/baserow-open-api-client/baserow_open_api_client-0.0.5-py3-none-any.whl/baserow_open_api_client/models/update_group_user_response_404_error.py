from enum import Enum


class UpdateGroupUserResponse404Error(str, Enum):
    ERROR_GROUP_USER_DOES_NOT_EXIST = "ERROR_GROUP_USER_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
