from enum import Enum


class ScopeTypeEnum(str, Enum):
    APPLICATION = "application"
    BUILDER = "builder"
    BUILDER_DOMAIN = "builder_domain"
    BUILDER_ELEMENT = "builder_element"
    BUILDER_PAGE = "builder_page"
    CORE = "core"
    DATABASE = "database"
    DATABASE_FIELD = "database_field"
    DATABASE_TABLE = "database_table"
    DATABASE_VIEW = "database_view"
    DATABASE_VIEW_DECORATION = "database_view_decoration"
    DATABASE_VIEW_FILTER = "database_view_filter"
    DATABASE_VIEW_SORT = "database_view_sort"
    SNAPSHOT = "snapshot"
    TEAM = "team"
    TEAM_SUBJECT = "team_subject"
    TOKEN = "token"
    WORKSPACE = "workspace"
    WORKSPACE_INVITATION = "workspace_invitation"
    WORKSPACE_USER = "workspace_user"

    def __str__(self) -> str:
        return str(self.value)
