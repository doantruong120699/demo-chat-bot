from rest_framework.views import APIView
from common.custom.success_response import success_response
from accounts.serializers.user import (
    ChangePasswordSerializer,
    UpdateUserSerializer,
    UserSerializer,
)
from rest_framework.permissions import IsAuthenticated


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return success_response(
            message="User fetched successfully", data=serializer.data
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="Password changed successfully")


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer(
            instance=request.user,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="User updated successfully")
