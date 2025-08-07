from enum import unique, Enum
from .base import AzooBaseEnum


@unique
class BannerStatusEnum(int, AzooBaseEnum):
    WAITING: int = 1
    POSTING: int = 2
    EXPIRED: int = 3
