from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Priority)
admin.site.register(Task)
admin.site.register(TaskUser)
admin.site.register(TimeInterval)
admin.site.register(Log)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'datetime_start', 'datetime_end', 'reason', 'status')
    search_fields = ('user__email', 'reason')
admin.site.register(Request, RequestAdmin)


admin.site.register(Notification)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'project__name', 'role_id')
    list_filter = ('project', 'role_id')
    search_fields = ('user__email', 'project__name')
    list_per_page = 20
admin.site.register(ProjectUser, ProjectUserAdmin)

admin.site.register(WarningReport)
admin.site.register(Setting)
