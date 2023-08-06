from enum import Enum


class UpdateTeamResponse404Error(str, Enum):
    ERROR_ROLE_DOES_NOT_EXIST = "ERROR_ROLE_DOES_NOT_EXIST"
    ERROR_SUBJECT_DOES_NOT_EXIST = "ERROR_SUBJECT_DOES_NOT_EXIST"
    ERROR_TEAM_DOES_NOT_EXIST = "ERROR_TEAM_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
