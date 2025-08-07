from enum import Enum


class MessageLevelEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
