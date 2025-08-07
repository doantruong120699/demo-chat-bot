from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.models.user import User
from accounts.services.google_oauth2 import GoogleOAuth2
from common.constant.user import UserStatusEnum
from common.utils.strings import generate_uuid


class SignUpGoogleSerializer(serializers.Serializer):
    google_access_token = serializers.CharField(max_length=255)

    def create(self, validated_data):
        google_access_token = validated_data["google_access_token"]
        google_auth = GoogleOAuth2()
        user_info = google_auth.get_user_details(google_access_token)

        user = User.objects.create_user(
            email=user_info.get("email"),
            username=generate_uuid(),
            fullname=user_info.get("name"),
            status=UserStatusEnum.ACTIVE,
            social_provider=User.SocialProvider.GOOGLE,
        )
        return user
