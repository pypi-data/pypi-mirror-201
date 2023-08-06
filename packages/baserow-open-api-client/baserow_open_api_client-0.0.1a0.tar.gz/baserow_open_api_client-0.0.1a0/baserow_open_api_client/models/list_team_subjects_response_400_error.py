from enum import Enum


class ListTeamSubjectsResponse400Error(str, Enum):
    ERROR_TEAM_DOES_NOT_EXIST = "ERROR_TEAM_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
