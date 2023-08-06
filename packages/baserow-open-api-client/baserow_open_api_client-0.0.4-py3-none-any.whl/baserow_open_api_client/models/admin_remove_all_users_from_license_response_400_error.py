from enum import Enum


class AdminRemoveAllUsersFromLicenseResponse400Error(str, Enum):
    ERROR_CANT_MANUALLY_CHANGE_SEATS = "ERROR_CANT_MANUALLY_CHANGE_SEATS"

    def __str__(self) -> str:
        return str(self.value)
