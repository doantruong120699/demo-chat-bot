from enum import Enum


class RegexPattern(str, Enum):
    PASS_REGEX = "^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^*])[a-zA-Z\d!@#$%^*]{10,20}$"
    ADMIN_TMP_PASS = (
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-+?_=,<>]).{16}$"
    )
    FULL_NAME_KANA = "^[ぁ-ん ]+$"
    SNAKE_CASE = "(?<!^)(?=[A-Z])"
    PHONE_NUMBER_REGEX = "^\+?1?\d{9,15}$"
    USERNAME = "^[a-z0-9_]{5,15}$"


class TokenManagement(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    ALGORITHM = "HS256"
    VERIFY_SIGNATURE = "verify_signature"


class TokenObtainPairEnum(str, Enum):
    CREATED_AT_LABEL = "created_at"


class SortTypeEnum(str, Enum):
    ASC = "ASC"
    DESC = "DESC"
