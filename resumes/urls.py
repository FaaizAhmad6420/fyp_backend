from django.urls import path
from .views import ResumeUploadView, GenerateTailoredResumeView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('generate-tailored-resume/', GenerateTailoredResumeView.as_view(), name='generate-tailored-resume'),
]
