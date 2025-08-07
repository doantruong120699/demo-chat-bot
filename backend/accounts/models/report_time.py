from django.db import models
from django.conf import settings

class ReportTime(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_times'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "report_time"
        verbose_name = "Report Time"
        verbose_name_plural = "Report Times"

    def __str__(self):
        return f"{self.user.email} | {self.start_time} - {self.end_time}"
