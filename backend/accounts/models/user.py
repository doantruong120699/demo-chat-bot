from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
)
from django.db import models

from common.constant.user import UserStatusEnum
from common.models.base import DateTimeModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.UserRole.SUPER_ADMIN)
        extra_fields.setdefault("status", User.UserStatus.ACTIVE)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin, DateTimeModel):
    class SocialProvider(models.TextChoices):
        GOOGLE = "google", "google"
        APPLE = "apple", "apple"
        FACEBOOK = "facebook", "facebook"
        NONE = "none", "none"

    class UserRole(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "SUPER_ADMIN"
        ADMIN = "ADMIN", "ADMIN"
        USER = "USER", "USER"

    class UserStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "ACTIVE"
        INACTIVE = "INACTIVE", "INACTIVE"
        BLOCKED = "BLOCKED", "BLOCKED"

    username = None
    first_name = None
    last_name = None
    groups = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    social_provider = models.CharField(
        max_length=32, choices=SocialProvider.choices, default=SocialProvider.NONE
    )
    status = models.CharField(choices=UserStatus.choices, default=UserStatus.INACTIVE)
    role = models.CharField(choices=UserRole.choices, default=UserRole.USER)
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.role in [self.UserRole.ADMIN, self.UserRole.SUPER_ADMIN]

    @property
    def is_superuser(self):
        return self.role in [self.UserRole.SUPER_ADMIN]

    class Meta:
        db_table = "users"
