from django.db import models
from django.contrib.auth import get_user_model

from resumes.models import Resume
from jobs.models import Job

User = get_user_model()


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("submitted", "Submitted"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    tailored_resume = models.TextField(
        blank=True
    )

    cover_letter = models.TextField(
        blank=True
    )

    ats_score = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"