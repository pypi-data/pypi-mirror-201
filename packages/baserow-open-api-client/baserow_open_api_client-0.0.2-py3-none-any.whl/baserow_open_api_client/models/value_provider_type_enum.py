from enum import Enum


class ValueProviderTypeEnum(str, Enum):
    CONDITIONAL_COLOR = "conditional_color"
    SINGLE_SELECT_COLOR = "single_select_color"

    def __str__(self) -> str:
        return str(self.value)
