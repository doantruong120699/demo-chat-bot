from enum import unique, Enum


@unique
class TransactionStatusEnum(int, Enum):
    TEMPORARY: int = 1
