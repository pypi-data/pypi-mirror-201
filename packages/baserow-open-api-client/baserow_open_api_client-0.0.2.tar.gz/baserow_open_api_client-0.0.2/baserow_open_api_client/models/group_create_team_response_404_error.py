from enum import Enum


class GroupCreateTeamResponse404Error(str, Enum):
    ERROR_GROUP_DOES_NOT_EXIST = "ERROR_GROUP_DOES_NOT_EXIST"
    ERROR_ROLE_DOES_NOT_EXIST = "ERROR_ROLE_DOES_NOT_EXIST"
    ERROR_SUBJECT_DOES_NOT_EXIST = "ERROR_SUBJECT_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
