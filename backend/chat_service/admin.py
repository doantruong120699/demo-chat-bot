from django.contrib import admin
from .models import Chat, Message
# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    list_per_page = 10
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')