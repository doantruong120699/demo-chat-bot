from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        depth = 5

class ChatHistoryListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid")
    class Meta:
        model = Chat
        fields = ["id", "title", "created_at", "updated_at"]

class ChatHistoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid")
    messages = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = ["id", "title", "created_at", "updated_at", "messages"]

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all().order_by("created_at"), many=True).data

class ChatRequestSerializer(serializers.Serializer):
    chat_id = serializers.CharField(required=True, allow_null=True)
    message = serializers.CharField(required=True)
