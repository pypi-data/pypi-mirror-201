from enum import Enum


class AdminDeleteGroupResponse400Error(str, Enum):
    ERROR_FEATURE_NOT_AVAILABLE = "ERROR_FEATURE_NOT_AVAILABLE"
    ERROR_GROUP_DOES_NOT_EXIST = "ERROR_GROUP_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
