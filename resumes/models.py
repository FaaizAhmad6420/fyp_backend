from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()  # This ensures we use the custom user model if any

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each resume belongs to a user
    file = models.FileField(upload_to='resumes/')            # Uploaded file saved in 'resumes/' folder
    extracted_text = models.TextField(blank=True)            # Stores extracted text from the resume
    skills = models.JSONField(default=list)                 # Stores skills as a list (JSON)
    created_at = models.DateTimeField(auto_now_add=True)     # Auto timestamp when uploaded

    def __str__(self):
        return f"{self.user.email} - {self.file.name}"
