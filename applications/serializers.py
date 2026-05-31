from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = "__all__"

    def get_job(self, obj):

        return {
            "id": obj.job.id,
            "title": obj.job.title,
            "company": obj.job.company,
            "location": obj.job.location,
        }
