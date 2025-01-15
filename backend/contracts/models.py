from django.db import models
# Create your models here.


class Contract(models.Model):
    job = models.OneToOneField('jobs.Job', on_delete=models.CASCADE)
    proposal = models.OneToOneField(
        'proposals.Proposal', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
