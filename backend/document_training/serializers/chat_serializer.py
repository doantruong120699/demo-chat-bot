from rest_framework import serializers
from document_training.models import ChatHistory


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for chat messages in history"""
    role = serializers.ChoiceField(choices=['user', 'assistant'])
    content = serializers.CharField()


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat request"""
    document_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(max_length=2000)
    chat_history = serializers.ListField(
        child=ChatMessageSerializer(),
        required=False,
        allow_empty=True,
    )
    session_id = serializers.CharField(required=False, allow_blank=True)
    
    # For uploading file content directly (without creating Document first)
    file_content = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    file_name = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)


class ChatWithFileSerializer(serializers.Serializer):
    """Serializer for chat with file upload (multipart/form-data)"""
    message = serializers.CharField(max_length=2000)
    file = serializers.FileField(required=False, allow_null=True)
    session_id = serializers.CharField(required=False, allow_blank=True)
    
    def validate_file(self, value):
        """Validate file size and type"""
        if value:
            # Max 10MB
            if value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("File size must not exceed 10MB")
            
            # Accept text files
            allowed_types = ['text/plain', 'application/pdf', 'application/json']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f"File type {value.content_type} not supported. "
                    f"Allowed: {', '.join(allowed_types)}"
                )
        return value


class ChatHistorySerializer(serializers.ModelSerializer):
    """Serializer for chat history model"""
    
    class Meta:
        model = ChatHistory
        fields = ['id', 'role', 'content', 'session_id', 'created_at']
        read_only_fields = ['id', 'created_at']
