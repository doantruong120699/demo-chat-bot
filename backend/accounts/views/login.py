from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from common.custom.success_response import success_response
from common.custom.exceptions import APIException
from accounts.serializers.login import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)
from rest_framework.permissions import IsAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        methods=["POST"],
        tags=["auth"],
        request=CustomTokenObtainPairSerializer,
    )
    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)
        return success_response(message="Login successful", data=data.data)


class CustomTokenRefreshView(TokenViewBase):
    serializer_class = CustomTokenRefreshSerializer

    @extend_schema(
        methods=["POST"],
        tags=["auth"],
        request=CustomTokenRefreshSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise APIException(e.args[0])

        return success_response(serializer.validated_data)


class CustomTokenLogoutView(TokenViewBase):
    serializer_class = CustomTokenRefreshSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=["POST"],
        tags=["auth"],
        request=CustomTokenRefreshSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise APIException(e.args[0])

        return success_response("Logout successful", None, 204)
