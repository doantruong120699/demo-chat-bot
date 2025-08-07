from io import BytesIO
from urllib.parse import urljoin
from django.core.files.storage import Storage
from common.aws.s3 import S3Storage
from django.conf import settings
import os
from uuid import uuid4

from common.constant.storage import FolderS3StorageEnum


class CustomStorage(Storage):

    def __init__(self, file_overwrite, default_folder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_overwrite = file_overwrite
        self.default_folder = default_folder
        self.s3_storage = S3Storage()
        if default_folder == FolderS3StorageEnum.PUBLIC.value:
            self.base_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/"
        else:
            self.base_url = settings.BACKEND_URL + "/media-proxy/"

    def deconstruct(self):
        """
        Return a 3-tuple of class import path, positional arguments,
        and keyword arguments.
        """
        path = "common.custom.storage.CustomStorage"
        args = []
        kwargs = {
            "file_overwrite": self.file_overwrite,
            "default_folder": self.default_folder,
        }
        return path, args, kwargs

    def get_available_name(self, name, max_length=None):
        """Generate a unique filename using UUID4."""
        ext = os.path.splitext(name)[1]
        return f"{uuid4()}{ext}"

    def _save(self, name: str, content: BytesIO):
        content.seek(0)
        name = self.get_available_name(name)

        path = self.s3_storage.upload_file(
            content=content,
            file_path=self.default_folder,
            file_name=name,
        )
        return os.path.join(self.default_folder, name)

    def exists(self, name):
        return False

    def url(self, name):
        if name.startswith(self.default_folder):
            return urljoin(self.base_url, name)
        return urljoin(self.base_url, f"{self.default_folder}/{name}")

    def size(self, name):
        """
        Return the total size, in bytes, of the file specified by name.
        """
        try:
            obj = self.s3_storage.get_object(name)
            return obj["ContentLength"]
        except Exception:
            return 0
