from rest_framework import serializers
from document_training.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Document serializer"""
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'language', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create document and set user from context"""
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
