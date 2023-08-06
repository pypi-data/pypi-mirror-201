from enum import Enum


class GetPublicViewInfoResponse401Error(str, Enum):
    ERROR_NO_AUTHORIZATION_TO_PUBLICLY_SHARED_VIEW = "ERROR_NO_AUTHORIZATION_TO_PUBLICLY_SHARED_VIEW"

    def __str__(self) -> str:
        return str(self.value)
