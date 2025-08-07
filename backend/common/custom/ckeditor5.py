from io import BytesIO
import os
from uuid import uuid4

from urllib.parse import urljoin

from django.conf import settings
from common.aws.s3 import S3Storage
from django.core.files.storage import Storage


class CustomCkeditor5Storage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_storage = S3Storage()
        self.base_url = settings.BACKEND_URL + "/media-proxy/"

    def get_available_name(self, name, max_length=None):
        """Generate a unique filename using UUID4."""
        ext = os.path.splitext(name)[1]
        return f"{uuid4()}{ext}"

    def _save(self, name: str, content: BytesIO):
        content.seek(0)
        self.s3_storage.upload_file(
            content=content,
            file_path="ckeditor5",
            file_name=name,
        )
        return f"ckeditor5/{name}"

    def exists(self, name):
        return False

    def url(self, name):
        return urljoin(self.base_url, name)
