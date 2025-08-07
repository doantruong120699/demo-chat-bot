from django.contrib import admin

# Register your models here.

from accounts.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "role",
        "created_at",
        "updated_at",
    )
    list_filter = ("role",)
    list_display_links = ("email",)
    search_fields = ("email",)
    ordering = ("-created_at",)
