from enum import Enum


class StateEnum(str, Enum):
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    EXPORTING = "exporting"
    FAILED = "failed"
    FINISHED = "finished"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
