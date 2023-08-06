from enum import Enum


class CreateSubjectResponse400Error(str, Enum):
    ERROR_SUBJECT_BAD_REQUEST = "ERROR_SUBJECT_BAD_REQUEST"
    ERROR_SUBJECT_NOT_IN_GROUP = "ERROR_SUBJECT_NOT_IN_GROUP"
    ERROR_SUBJECT_TYPE_UNSUPPORTED = "ERROR_SUBJECT_TYPE_UNSUPPORTED"

    def __str__(self) -> str:
        return str(self.value)
