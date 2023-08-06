from enum import Enum


class AdminAddUserToLicenseResponse400Error(str, Enum):
    ERROR_CANT_MANUALLY_CHANGE_SEATS = "ERROR_CANT_MANUALLY_CHANGE_SEATS"
    ERROR_NO_SEATS_LEFT_IN_LICENSE = "ERROR_NO_SEATS_LEFT_IN_LICENSE"
    ERROR_USER_ALREADY_ON_LICENSE = "ERROR_USER_ALREADY_ON_LICENSE"

    def __str__(self) -> str:
        return str(self.value)
