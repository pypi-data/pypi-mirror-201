from enum import Enum


class DeleteSnapshotResponse404Error(str, Enum):
    ERROR_SNAPSHOT_DOES_NOT_EXIST = "ERROR_SNAPSHOT_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
