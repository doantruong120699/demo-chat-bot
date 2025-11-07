from django.contrib import admin
from .models import Document, ChatHistory, ChatSession


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'language', 'created_at']
    list_filter = ['language', 'created_at']
    search_fields = ['title', 'user__email', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'title', 'language')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'title', 'user', 'document', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'language', 'created_at']
    search_fields = ['session_id', 'title', 'user__email', 'document__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('id', 'session_id', 'user', 'title', 'is_active')
        }),
        ('Document Snapshot', {
            'fields': ('document', 'document_title', 'document_content', 'language')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'session__session_id', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
