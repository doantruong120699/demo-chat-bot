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
admin.site.register(Request)
admin.site.register(Notification)
admin.site.register(ProjectUser)
admin.site.register(WarningReport)
admin.site.register(Setting)
