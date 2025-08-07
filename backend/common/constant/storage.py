from enum import Enum


class StorageField(str, Enum):
    FILE = "file"
    FILE_NAME = "file_name"
    FILE_NAME_UUID = "file_name_uuid"
    FILE_TYPE = "file_type"
    FILE_CONTENT = "file_content"
    UPLOAD_PATH = "upload_path"
    UPLOAD_TYPE = "upload_type"
    URL = "url"
    DEFAULT_ACL = "default_acl"
    BUCKET_NAME = "bucket_name"
    PROTECTED = "protected"
    IS_RENAME = "is_rename"
    DEFAULT_FOLDER = "default_folder"
    KEY_FOLDER = "key_folder"


class UploadTypeEnum(str, Enum):
    MEDIA = "media"
    TEMP = "tmp"
    YW_API = "yw_api"
    PUBLIC = "public"


class ACLsStorageEnum(str, Enum):
    PRIVATE = "private"
    PUBLIC_READ = "public-read"


class FolderS3StorageEnum(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    S3 = "s3"
    S3_URL = "/s3"
    MEDIA = "public/media"
    TEMP = "/" + "tmp" + "/"


class FileSizeEnum(int, Enum):
    BYTE = 1024
