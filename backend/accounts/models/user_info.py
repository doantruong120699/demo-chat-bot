from django.db import models

from accounts.models.user import User


class UserInfo(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_info"
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=5000, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    # salary
    salary = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "user_info"
