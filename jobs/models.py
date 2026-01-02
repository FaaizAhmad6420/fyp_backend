from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField()
    source = models.CharField(max_length=50)  # e.g., "RemoteOK", "CareerJet"
    skills = models.JSONField(default=list)  # list of skills required
    url = models.URLField(max_length=500, blank=True, null=True)  # optional: link to job posting
    fetched_at = models.DateTimeField(auto_now_add=True)  # when job was fetched

    def __str__(self):
        return f"{self.title} at {self.company}"
