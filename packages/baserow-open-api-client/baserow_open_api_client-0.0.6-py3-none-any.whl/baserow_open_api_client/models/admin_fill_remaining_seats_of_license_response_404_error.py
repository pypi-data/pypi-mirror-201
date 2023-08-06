from enum import Enum


class AdminFillRemainingSeatsOfLicenseResponse404Error(str, Enum):
    ERROR_LICENSE_DOES_NOT_EXIST = "ERROR_LICENSE_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
