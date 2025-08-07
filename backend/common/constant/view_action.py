from enum import Enum


class ViewSetAction(str, Enum):
    LIST = "list"
    DETAIL = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    PATCH = "patch"
    UPDATE_STATUS = "update_status"
    DELETE = "destroy"
    EXPORT_CSV = "export_csv"
    STATISTICS = "statistics"
    LIST_NON_PAGINATION = "list_non_pagination"
    LIST_BY_CATEGORY = "list_by_category"

    DELETE_MULTIPLE = "delete_multiple"
    UPDATE_MULTIPLE = "update_multiple"
    DELETE_WITH_CONDITION = "delete_with_conditions"
