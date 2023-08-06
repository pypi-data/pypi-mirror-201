from enum import Enum


class GetJobResponse404Error(str, Enum):
    ERROR_JOB_DOES_NOT_EXIST = "ERROR_JOB_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
