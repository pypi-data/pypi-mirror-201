from enum import Enum


class AggregationRawTypeEnum(str, Enum):
    AVERAGE = "average"
    DECILE = "decile"
    EMPTY_COUNT = "empty_count"
    MAX = "max"
    MEDIAN = "median"
    MIN = "min"
    NOT_EMPTY_COUNT = "not_empty_count"
    STD_DEV = "std_dev"
    SUM = "sum"
    UNIQUE_COUNT = "unique_count"
    VARIANCE = "variance"

    def __str__(self) -> str:
        return str(self.value)
