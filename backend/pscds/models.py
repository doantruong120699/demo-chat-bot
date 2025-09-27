from django.db import models
# from django.contrib.gis.db import models as gis_models  # for PointField (GeoDjango)


class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    url = models.CharField(max_length=255, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    screenshots_active = models.IntegerField(default=0)
    manual_time = models.IntegerField(default=0)
    computer_time_popup = models.IntegerField(default=0)
    blur_screenshots = models.IntegerField(default=0)
    web_and_app_monitoring = models.BooleanField(default=False)
    screenshots_interval = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    important = models.BooleanField(default=False)
    change_password = models.BooleanField(default=False)
    role_id = models.IntegerField(blank=True, null=True)
    user_language = models.CharField(max_length=255, blank=True, null=True)
    invitation_sent = models.BooleanField(default=False)
    nonce = models.IntegerField(blank=True, null=True)
    client_installed = models.BooleanField(default=False)
    permanent_screenshots = models.BooleanField(default=False)
    last_activity = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    remember_me_identity = models.CharField(max_length=255, blank=True, null=True)
    remember_me_token = models.CharField(max_length=255, blank=True, null=True)
    datebirth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_users"

    def __str__(self):
        return self.full_name


class Project(models.Model):
    company_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.IntegerField(default=0)
    in_progress = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(blank=True, null=True)
    import_field = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    default_priority_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_projects"

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_priorities"

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.TextField()
    description = models.TextField(blank=True, null=True)
    work_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    warning_time = models.FloatField(default=0)
    assigned_by = models.IntegerField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    status_id = models.IntegerField(default=0)
    relative_position = models.DecimalField(max_digits=64, decimal_places=30, default=0)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)
    users = models.ManyToManyField(User, through="TaskUser")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_tasks"

    def __str__(self):
        return self.task_name


class TaskUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_tasks_users"


class TimeInterval(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="time_intervals")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    different_timezone = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)
    activity_fill = models.IntegerField(default=0)
    mouse_fill = models.IntegerField(default=0)
    keyboard_fill = models.IntegerField(default=0)
    # location = gis_models.PointField(blank=True, null=True)
    job = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_time_intervals"


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    event = models.TextField()
    sit = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    os = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_logs"


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    reason = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_requests"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    type = models.IntegerField()
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=[('unread', 'Unread'), ('ready', 'Ready')],
        default='unread'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_notifications"


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.IntegerField(blank=True, null=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_projects_users"


class WarningReport(models.Model):
    report_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pscds_warning_reports"


class Setting(models.Model):
    module_name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pscds_settings"
