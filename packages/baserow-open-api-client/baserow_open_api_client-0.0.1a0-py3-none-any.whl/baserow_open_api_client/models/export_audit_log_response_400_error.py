from enum import Enum


class ExportAuditLogResponse400Error(str, Enum):
    ERROR_MAX_JOB_COUNT_EXCEEDED = "ERROR_MAX_JOB_COUNT_EXCEEDED"
    ERROR_REQUEST_BODY_VALIDATION = "ERROR_REQUEST_BODY_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)
