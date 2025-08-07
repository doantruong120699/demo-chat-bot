# common/backends.py

from django.contrib.auth.backends import ModelBackend


class RoleBasedAdminBackend(ModelBackend):
    def user_can_authenticate(self, user):
        is_valid = super().user_can_authenticate(user)
        return is_valid and user.role in ["ADMIN", "SUPER_ADMIN"]
