from enum import Enum


class AcceptGroupInvitationResponse400Error(str, Enum):
    ERROR_GROUP_INVITATION_EMAIL_MISMATCH = "ERROR_GROUP_INVITATION_EMAIL_MISMATCH"

    def __str__(self) -> str:
        return str(self.value)
