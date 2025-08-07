from os.path import basename
from typing import Any, Dict, Tuple
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import ForeignKey

from common.constant.constant import RegexPattern
from common.constant.storage import (
    FolderS3StorageEnum,
    FileSizeEnum,
    StorageField,
)
from common.models.managers import CustomUserManager
from common.custom.exceptions import APIError
from common.utils.middleware import get_current_user
import uuid


class CurrentUserField(ForeignKey):
    def __init__(self, to="accounts.User", provider="admin", **kwargs):
        self.auto_current = kwargs.pop("auto_current", False)
        self.auto_current_add = kwargs.pop("auto_current_add", False)
        super().__init__(to, **kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_current or (self.auto_current_add and add):
            current_user = get_current_user()
            # Handle normal case
            if current_user and current_user.is_authenticated:
                user_id = current_user.id
                setattr(model_instance, "editor_admin_id", None)
                setattr(model_instance, "editor_user_id", None)
                setattr(model_instance, self.attname, user_id)
                return user_id

        return super().pre_save(model_instance, add)


class UserCreator(models.Model):
    creator_user = CurrentUserField(
        to="user.User",
        provider="user",
        auto_current_add=True,
        null=True,
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_creator_user",
    )

    class Meta:
        abstract = True


class UserEditor(models.Model):
    editor_user = CurrentUserField(
        to="user.User",
        provider="user",
        auto_current=True,
        null=True,
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_editor_user",
    )

    class Meta:
        abstract = True


class TrackingIPModel(models.Model):
    ip = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("Ngày tạo")
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("Ngày cập nhật")
    )

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(
        default=False, verbose_name=_("Đã xóa"), help_text=_("Đã xóa")
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.is_deleted = True
        self.save()


class UuidModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["uuid"])]


class CustomBaseUserModel(AbstractBaseUser, DateTimeModel, SoftDeleteModel):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        abstract = True


class MaterBaseModel(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class FileBaseModel(models.Model):
    class Meta:
        abstract = True

    def __validate_file_size_from_s3(self, s3_storage, to_path):
        size_file = s3_storage.get_size_file(to_path=to_path)
        if (
            size_file
            and size_file
            > self.UPLOAD_SIZE_LIMIT * FileSizeEnum.BYTE * FileSizeEnum.BYTE
        ):
            raise APIError(f"Max file size is {self.UPLOAD_SIZE_LIMIT}MB")

    def __get_path_s3_save_file(self, file, s3_storage):
        key_folder = getattr(self, StorageField.KEY_FOLDER.value, self.pk)
        from_path = (
            s3_storage.default_folder
            + file.name.split(s3_storage.default_folder)[-1].split("?")[0]
        )
        to_path = f'{s3_storage.default_folder}/{self.UPLOAD_TO}/{key_folder}/{basename(file.name).split("?")[0]}'
        self.__validate_file_size_from_s3(s3_storage, from_path)
        return from_path, to_path

    def save_file(self, *args, **kwargs):
        if not self.pk:
            super(self.__class__, self).save(*args, **kwargs)
            kwargs = {}

        for field in self.__class__._meta.get_fields():
            if isinstance(field, models.FileField) or isinstance(
                field, models.ImageField
            ):
                file_taken = getattr(self, field.name)
                s3_storage = field.storage

                if (
                    file_taken
                    and s3_storage
                    and s3_storage.default_folder in file_taken.name
                ):
                    from_path, to_path = self.__get_path_s3_save_file(
                        file_taken, s3_storage
                    )
                    # step move file
                    if FolderS3StorageEnum.TEMP in file_taken.name:
                        s3_storage.copy(from_path=from_path, to_path=to_path)
                    setattr(self, field.name, to_path)

        super(self.__class__, self).save(*args, **kwargs)


class TrackerModel(UuidModel, DateTimeModel, TrackingIPModel):
    req_uuid = models.UUIDField(null=True)
    # Owner record
    owner_uuid = models.UUIDField(null=True, blank=True)
    owner_username = models.CharField(max_length=255, null=True, blank=True)
    owner_provider = models.CharField(max_length=50, null=True)
    # executor
    executor_uuid = models.UUIDField(null=True, blank=True)
    executor_username = models.CharField(max_length=255, null=True, blank=True)
    executor_provider = models.CharField(max_length=50, null=True)
    # Target model
    instance_uuid = models.UUIDField(null=True)
    # Data change
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    # action = models.IntegerField(
    #     choices=TrackingActionEnum.choices(), null=True)

    class Meta:
        abstract = True
