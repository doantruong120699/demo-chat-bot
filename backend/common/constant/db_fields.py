from enum import Enum


class DBMasterFields(str, Enum):
    ID = "id"
    NAME = "name"


class DBAdminFields(str, Enum):
    ID = "id"
    EMAIL = "email"
    USERNAME = "username"
    PASSWORD = "password"
    NAME = "name"
    IS_ACTIVE = "is_active"
    ROLE_ID = "role_id"
    ROLE_NAME = "role_name"
    ROLE = "role"
    CREATED_DATE = "created_at"
    UPDATED_DATE = "updated_at"
    SET_PASSWORD_FLAG = "set_password_flag"
    EDITOR_STAFF_ID = "editor_admin_id"
    EDITOR_STAFF_NAME = "editor_admin_name"
    IS_SUPER_ADMIN = "is_super_admin"
    PERMISSIONS = "permissions"


class DBAdminPermissionFields(str, Enum):
    ID = "id"
    MODULE_ID = "module_id"
    MODULE_NAME = "module_name"
    ACTION = "action"
    ACTIONS = "actions"
    # NAME = 'name'


class DBFieldsCommon(str, Enum):
    ID = "id"
    EMAIL = "email"
    USERNAME = "username"
    TOKEN = "token"
    PASSWORD = "password"
    NEW_PASSWORD = "new_password"
    OLD_PASSWORD = "old_password"
    USER = "user"
    REGISTRATION_STEP = "registration_step"
    APPROVED_BY = "approved_by"
    STATUS_NAME = "status_name"
    EDITOR_INFO = "editor_info"
    IS_DELETED = "is_deleted"
    IS_ACTIVE = "is_active"
    STATUS_ID = "status_id"
    IS_VERIFY_EMAIL = "is_verified_mail"
    IS_SUPER_ADMIN = "is_super_admin"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class DBUserFields(str, Enum):
    ID = "id"
    EMAIL = "email"
    USERNAME = "username"
    FULLNAME = "fullname"
    TOKEN = "token"
    PASSWORD = "password"
    IS_ACTIVE = "is_active"
    OTP = "otp"
    TYPE = "type"
    ROLE = "role"
    COUNTRY = "country"
    COUNTRY_ID = "country_id"
    INDIVIDUAL = "individual"
    COMPANY = "company"
    CORPORATION = "corporation"
    ORGANIZATION = "organization"
    PHONE = "phone"
    IS_SELLER = "is_seller"
    SELLER_STATUS = "seller_status"
    STATUS = "status"
    POINT = "point"


class DBUserRoleFields(str, Enum):
    ID = "id"
    NAME = "name"


class DBIndividualFields(str, Enum):
    ID = "id"
    BIRTHDAY = "birthday"
    USER = "user"


class DBCompanyFields(str, Enum):
    ID = "id"
    USER = "user"
    COMPANY_NAME = "company_name"
    COMPANY_ADDRESS = "company_address"
    COMPANY_ADDRESS_DETAIL = "company_address_detail"
    COMPANY_PAGE = "company_page"
    COMPANY_CODE = "company_code"
    COMPANY_CERTIFICATE = "company_certificate"
    REPRESENTATIVE_NAME = "representative_name"
    REPRESENTATIVE_CARD = "representative_card"
    DEPARTMENT = "department"
    POSITION = "position"


class DBCorporationFields(str, Enum):
    ID = "id"
    USER = "user"
    CORPORATION_NAME = "corporation_name"
    CORPORATION_ADDRESS = "corporation_address"
    CORPORATION_ADDRESS_DETAIL = "corporation_address_detail"
    CORPORATION_PAGE = "corporation_page"
    CORPORATION_CODE = "corporation_code"
    CORPORATION_CERTIFICATE = "corporation_certificate"
    SHARE_HOLDER = "share_holder"
    REPRESENTATIVE_NAME = "representative_name"
    REPRESENTATIVE_CARD = "representative_card"
    DEPARTMENT = "department"
    POSITION = "position"
