from enum import Enum


class GetDatabaseTableGridViewFieldAggregationResponse400Error(str, Enum):
    ERROR_AGGREGATION_TYPE_DOES_NOT_EXIST = "ERROR_AGGREGATION_TYPE_DOES_NOT_EXIST"
    ERROR_FIELD_NOT_IN_TABLE = "ERROR_FIELD_NOT_IN_TABLE"
    ERROR_USER_NOT_IN_GROUP = "ERROR_USER_NOT_IN_GROUP"

    def __str__(self) -> str:
        return str(self.value)
