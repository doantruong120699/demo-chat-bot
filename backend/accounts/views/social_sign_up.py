import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes

from accounts.services.user import UserAuthService
from common.constant.swagger_tags import SwaggerTag
from accounts.serializers.social_sign_up import SignUpGoogleSerializer
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.custom.success_response import success_response

logger = logging.getLogger(__name__)


@extend_schema(
    methods=["POST"],
    tags=[SwaggerTag.AUTH.value],
    request=SignUpGoogleSerializer,
    description="auth_google_callback",
)
@api_view(["POST"])
@permission_classes([])
def auth_google_callback(request):
    serializer = SignUpGoogleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_auth_service = UserAuthService()
    response = user_auth_service.google_sign_up(
        serializer.validated_data["google_access_token"]
    )
    return success_response(
        "Google sign up successfully", response, status_code=status.HTTP_200_OK
    )
