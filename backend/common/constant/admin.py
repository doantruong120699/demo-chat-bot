from enum import unique, Enum


@unique
class AdminStatusEnum(int, Enum):
    ACTIVE: int = 1
    BLOCKED: int = 2


@unique
class AdminRoleEnum(int, Enum):
    LEVEL_1: int = 1
    LEVEL_2: int = 2
    LEVEL_3: int = 3
