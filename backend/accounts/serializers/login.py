import logging

from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenBackendError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.state import token_backend

from accounts.models.user import User
from accounts.serializers.user import UserSerializer
from common.constant.message_code import auth_message
from common.custom.exceptions import APIError


logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    provider = None

    def get_token(self, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["access_token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        data["user"] = self.get_me(self.user)
        return data

    def get_me(self, user):
        logger.debug("Service: get me called. with user: %s", user)
        user_info = UserSerializer(user).data
        logger.debug("Service: get me called success")
        return user_info


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    """

    def validate(self, attrs):
        try:
            token = token_backend.decode(attrs["refresh"])
            User.objects.get(pk=token["user_id"])
        except TokenBackendError:
            raise APIError(_("Token is invalid or expired"))
        except User.DoesNotExist:
            raise APIError(auth_message.THE_USER_HAD_BEEN_DELETED_FROM_THE_SYSTEM)

        return super().validate(attrs)
