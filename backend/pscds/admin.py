from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Priority)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'project__name', 'status_id')
    list_filter = ('project', 'status_id')
    search_fields = ('task_name', 'project__name')
admin.site.register(Task, TaskAdmin)

# admin.site.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('task__task_name', 'user__email')
    list_filter = ('task', 'user')
    search_fields = ('task__task_name', 'user__email')
admin.site.register(TaskUser, TaskUserAdmin)

class TimeIntervalAdmin(admin.ModelAdmin):
    list_display = ('user__email','task', 'start_at', 'end_at')
    list_filter = ('task', 'user')
    search_fields = ('task__name', 'user__email')

admin.site.register(TimeInterval, TimeIntervalAdmin)
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
