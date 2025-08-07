from enum import unique, Enum
from .base import AzooBaseEnum


@unique
class UserTypeEnum(int, AzooBaseEnum):
    DOMESTIC: int = 1
    OVERSEAS: int = 2


@unique
class UserStatusEnum(int, AzooBaseEnum):
    INACTIVE: int = 1
    ACTIVE: int = 2
    BLOCKED: int = 3
    CANCEL: int = 4


@unique
class UserRoleEnum(int, AzooBaseEnum):
    INDIVIDUAL: int = 1
    COMPANY: int = 2
    CORPORATION: int = 3
    ORGANIZATION: int = 4


@unique
class UserRequestSellerStatusEnum(int, AzooBaseEnum):
    NOT_REQUEST: int = 1
    REQUESTED: int = 2
    APPROVED: int = 3
    DECLINE: int = 4
