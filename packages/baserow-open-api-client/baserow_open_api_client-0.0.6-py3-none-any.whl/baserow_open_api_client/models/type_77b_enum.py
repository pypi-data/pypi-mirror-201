from enum import Enum


class Type77BEnum(str, Enum):
    BOOLEAN = "boolean"
    CREATED_ON = "created_on"
    DATE = "date"
    EMAIL = "email"
    FILE = "file"
    FORMULA = "formula"
    LAST_MODIFIED = "last_modified"
    LINK_ROW = "link_row"
    LONG_TEXT = "long_text"
    LOOKUP = "lookup"
    MULTIPLE_COLLABORATORS = "multiple_collaborators"
    MULTIPLE_SELECT = "multiple_select"
    NUMBER = "number"
    PHONE_NUMBER = "phone_number"
    RATING = "rating"
    SINGLE_SELECT = "single_select"
    TEXT = "text"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
