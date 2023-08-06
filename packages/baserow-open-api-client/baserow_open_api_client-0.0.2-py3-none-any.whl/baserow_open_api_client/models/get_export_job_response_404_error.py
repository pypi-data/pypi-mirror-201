from enum import Enum


class GetExportJobResponse404Error(str, Enum):
    ERROR_EXPORT_JOB_DOES_NOT_EXIST = "ERROR_EXPORT_JOB_DOES_NOT_EXIST"

    def __str__(self) -> str:
        return str(self.value)
