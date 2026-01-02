from django.urls import path
from .views import FetchJobsView, JobMatchView

urlpatterns = [
    path("fetch/", FetchJobsView.as_view(), name="fetch_jobs"),
    path("match/", JobMatchView.as_view(), name="job_match"),
]