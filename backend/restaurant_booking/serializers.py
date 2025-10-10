from rest_framework import serializers

class RestaurantBookingChatRequestSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)
    chat_history = serializers.JSONField(required=True)
