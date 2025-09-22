from django.contrib import admin

# Register your models here.

from accounts.models.user import User
from accounts.models.user_info import UserInfo

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "role",
        "get_phone_number",
        "get_address",
        "get_profile_picture",
        "get_salary",
        "created_at",
        "updated_at",
    )
    list_filter = ("role",)
    list_display_links = ("email",)
    search_fields = ("email",)
    ordering = ("-created_at",)

    def get_phone_number(self, obj):
        """Get phone number from related UserInfo"""
        return obj.user_info.phone_number if hasattr(obj, 'user_info') and obj.user_info else None
    get_phone_number.short_description = 'Phone Number'

    def get_address(self, obj):
        """Get address from related UserInfo"""
        return obj.user_info.address if hasattr(obj, 'user_info') and obj.user_info else None
    get_address.short_description = 'Address'

    def get_profile_picture(self, obj):
        """Get profile picture from related UserInfo"""
        if hasattr(obj, 'user_info') and obj.user_info and obj.user_info.profile_picture:
            return f"<img src='{obj.user_info.profile_picture.url}' width='50' height='50' />"
        return "No image"
    get_profile_picture.short_description = 'Profile Picture'
    get_profile_picture.allow_tags = True

    def get_salary(self, obj):
        """Get salary from related UserInfo"""
        return obj.user_info.salary if hasattr(obj, 'user_info') and obj.user_info else None
    get_salary.short_description = 'Salary'

    
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
        "address",
        "profile_picture",
        "salary",
    )
    list_display_links = ("user",)
    search_fields = ("user__email",)