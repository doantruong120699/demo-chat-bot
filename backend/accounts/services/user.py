import logging

from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from accounts.models.user import User
from accounts.models.user_info import UserInfo
from accounts.serializers.user import UserSerializer
from accounts.services.google_oauth2 import GoogleOAuth2
from common.constant.constant import TokenObtainPairEnum
from common.constant.mail import MailTemplateEnum
from common.services.otp_service import OTPService
from common.utils.strings import get_current_time
from common.services.mail_service import MailService
from typing_extensions import TypedDict
from common.constant.user import UserStatusEnum

logger = logging.getLogger(__name__)


class TokenGenerateData(TypedDict):
    access_token: str
    refresh_token: str


class UserAuthService:

    def __init__(self):
        super(UserAuthService, self).__init__()
        self._mail_service = MailService()
        self._otp_service = OTPService()
        self._google_auth = GoogleOAuth2()

    def generate_auth_token(self, user) -> TokenGenerateData:
        refresh = RefreshToken.for_user(user)
        refresh[TokenObtainPairEnum.CREATED_AT_LABEL.value] = str(get_current_time())
        user_details = UserSerializer(user).data
        user.last_login = get_current_time()
        user.save(update_fields=["last_login"])
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": user_details,
        }

    def google_sign_up(self, google_access_token):
        user_info = self._google_auth.get_user_details(google_access_token)
        (user, created) = User.objects.get_or_create(
            email=user_info.get("email"),
            defaults={
                "full_name": (
                    f"{user_info.get('given_name')} {user_info.get('family_name')}"
                ),
                "status": UserStatusEnum.ACTIVE,
                "social_provider": User.SocialProvider.GOOGLE,
            },
        )

        token = self.generate_auth_token(user)
        return token

    def sign_up(self, user_data):
        user_data["password"] = make_password(user_data["password"])
        user_data["status"] = UserStatusEnum.INACTIVE
        phone_number = user_data.pop("phone_number")
        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            UserInfo.objects.create(user=user, phone_number=phone_number)
        # Send active email
        uidb64, token = self._generate_token(user)
        self._mail_service.send_email_template_by_type(
            email_type_enum=MailTemplateEnum.VERIFY_EMAIL,
            recipient_mails=[user.email],
            context={
                "callback_url": f"{settings.WEBSITE_URL}/verify-email?uidb64={uidb64}&token={token}",
            },
        )
        return user

    def active_account(self, uidb64):
        user, is_valid = self._verify_token(uidb64)
        if not user:
            raise ValueError("User not found")
        user.status = UserStatusEnum.ACTIVE
        user.save()
        return {"user": UserSerializer(user).data}

    def _generate_token(self, user):
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        return uidb64, token

    def _verify_token(self, uidb64, token=None):
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
        if token:
            return (user, PasswordResetTokenGenerator().check_token(user, token))
        return (user, None)
