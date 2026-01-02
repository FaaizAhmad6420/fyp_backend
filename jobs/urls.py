from django.urls import path
from .views import FetchJobsView, JobMatchView, GetJobsView

urlpatterns = [
    path("", GetJobsView.as_view(), name="jobs"),
    path("fetch/", FetchJobsView.as_view(), name="fetch_jobs"),
    path("match/", JobMatchView.as_view(), name="job_match"),
]