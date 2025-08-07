from rest_framework import serializers

from accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "phone_number"]
        extra_kwargs = {
            "password": {"write_only": True},
            "phone_number": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value


class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
