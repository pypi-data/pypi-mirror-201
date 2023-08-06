from enum import Enum


class AdminAddUserToLicenseResponse404Error(str, Enum):
    ERROR_LICENSE_DOES_NOT_EXIST = "ERROR_LICENSE_DOES_NOT_EXIST"
    ERROR_USER_NOT_FOUND = "ERROR_USER_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
