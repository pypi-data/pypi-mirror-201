from enum import Enum


class GetWorkspaceInvitationByTokenResponse400Error(str, Enum):
    BAD_TOKEN_SIGNATURE = "BAD_TOKEN_SIGNATURE"

    def __str__(self) -> str:
        return str(self.value)
