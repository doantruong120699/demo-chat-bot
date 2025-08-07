from accounts.models.user import User
from accounts.serializers.sign_up import SignUpSerializer, VerifyEmailSerializer
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from accounts.services.user import UserAuthService
from common.custom.success_response import success_response


class SignUpView(APIView):
    """
    API View for user registration
    """

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service = UserAuthService()
        user = user_service.sign_up(serializer.validated_data)
        return success_response(
            "User created successfully",
            serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    @swagger_auto_schema(request_body=VerifyEmailSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service = UserAuthService()
        resp = user_service.active_account(serializer.validated_data["uidb64"])
        return success_response(
            "Email verified successfully", resp, status_code=status.HTTP_200_OK
        )
