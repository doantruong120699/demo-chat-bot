from enum import unique, Enum
from .base import AzooBaseEnum


@unique
class CategoryStatusEnum(int, AzooBaseEnum):
    ACTIVE: int = 1
    BLOCKED: int = 2
