from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 stars

    contract = models.ForeignKey(
        'contracts.Contract',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="The contract related to this review"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        help_text="The user who writes this review"
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        help_text="The user being reviewed"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text="Rating given by the reviewer (1 to 5 stars)"
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        help_text="Optional textual feedback"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('contract', 'reviewer', 'reviewee')
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewee} (Contract: {self.contract})"
