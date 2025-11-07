from rest_framework import serializers
from document_training.models import ChatSession


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for chat session"""
    
    message_count = serializers.IntegerField(read_only=True, required=False)
    last_message_time = serializers.DateTimeField(read_only=True, required=False)
    preview = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = ChatSession
        fields = [
            'id',
            'session_id',
            'document',
            'document_title',
            'title',
            'language',
            'is_active',
            'created_at',
            'updated_at',
            'message_count',
            'last_message_time',
            'preview',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'document_content']
    
    def create(self, validated_data):
        """Create session with document snapshot"""
        document = validated_data.get('document')
        
        # Snapshot document content if document provided
        if document:
            validated_data['document_title'] = document.title
            validated_data['document_content'] = document.content
        
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)


class ChatSessionDetailSerializer(ChatSessionSerializer):
    """Detailed serializer with document content snapshot"""
    
    class Meta(ChatSessionSerializer.Meta):
        fields = ChatSessionSerializer.Meta.fields + ['document_content']
