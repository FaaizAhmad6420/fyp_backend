from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'extracted_text', 'skills', 'created_at']
        read_only_fields = ['user', 'extracted_text', 'skills', 'created_at']
