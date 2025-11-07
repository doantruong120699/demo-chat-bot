from django.db import models
from accounts.models.user import User
from pgvector.django import VectorField
import uuid


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Document(TimeStampedModel):
    """Document with text content for training"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_documents')
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Document text content")
    language = models.CharField(max_length=10, default='vi')
    
    class Meta:
        db_table = 'document_training_documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.user.email})"


class DocumentChunk(TimeStampedModel):
    """Chunked text segments with vector embeddings for semantic search"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    
    # Chunk content
    content = models.TextField(help_text="Text content of this chunk")
    chunk_index = models.IntegerField(help_text="Order of this chunk in the document")
    
    # Vector embedding (1536 dimensions for OpenAI ada-002)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    
    # Metadata
    token_count = models.IntegerField(default=0, help_text="Approximate token count")
    
    class Meta:
        db_table = 'document_training_chunks'
        ordering = ['document', 'chunk_index']
        indexes = [
            models.Index(fields=['document', 'chunk_index']),
        ]
    
    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"


class ChatSession(TimeStampedModel):
    """Chat session with document snapshot"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    
    # Document reference và snapshot
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, related_name='sessions', null=True, blank=True)
    document_title = models.CharField(max_length=255, null=True, blank=True, help_text="Snapshot of document title")
    document_content = models.TextField(null=True, blank=True, help_text="Snapshot of document content at session creation")
    
    # Session metadata
    title = models.CharField(max_length=255, null=True, blank=True, help_text="Session title (auto-generated or user-set)")
    language = models.CharField(max_length=10, default='vi')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'document_training_sessions'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"Session {self.session_id[:8]} - {self.title or 'Untitled'}"


class ChatHistory(TimeStampedModel):
    """Chat history for document Q&A"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    # Backward compatibility - có thể null nếu dùng session
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chat_history', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_chats')
    
    # Message content
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    
    class Meta:
        db_table = 'document_training_chat_history'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
    
    @property
    def session_id(self):
        """Backward compatibility property"""
        return self.session.session_id if self.session else None
