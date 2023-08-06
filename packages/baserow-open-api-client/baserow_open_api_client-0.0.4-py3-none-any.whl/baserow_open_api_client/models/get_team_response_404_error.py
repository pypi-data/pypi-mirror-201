from enum import Enum


class GetTeamResponse404Error(str, Enum):
    ERROR_TEAM_DOES_NOT_EXIST = "ERROR_TEAM_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
