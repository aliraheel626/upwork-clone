from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# Create your models here.


class Job(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255, default='')
    rate = models.IntegerField(default=0)
    description = models.TextField(default='')
    days_required = models.IntegerField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
