from enum import Enum


class ListSnapshotsResponse404Error(str, Enum):
    ERROR_APPLICATION_DOES_NOT_EXIST = "ERROR_APPLICATION_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
