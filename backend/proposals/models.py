from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Proposal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='proposals')
    description = models.TextField(default='')
    rate = models.IntegerField(default=0)
    days_required = models.IntegerField(default=0)
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='proposals')

    class Meta:
        # Enforces one proposal per user per job
        unique_together = ('user', 'job')
