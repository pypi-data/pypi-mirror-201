from enum import Enum


class Type7F3Enum(str, Enum):
    AIRTABLE = "airtable"
    AUDIT_LOG_EXPORT = "audit_log_export"
    CREATE_SNAPSHOT = "create_snapshot"
    DUPLICATE_APPLICATION = "duplicate_application"
    DUPLICATE_FIELD = "duplicate_field"
    DUPLICATE_PAGE = "duplicate_page"
    DUPLICATE_TABLE = "duplicate_table"
    FILE_IMPORT = "file_import"
    INSTALL_TEMPLATE = "install_template"
    RESTORE_SNAPSHOT = "restore_snapshot"

    def __str__(self) -> str:
        return str(self.value)
