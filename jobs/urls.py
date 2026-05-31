from django.urls import path
from .views import FetchJobsView, JobDetailView, JobMatchView, GetJobsView

urlpatterns = [
    path("", GetJobsView.as_view(), name="jobs"),
    path("fetch/", FetchJobsView.as_view(), name="fetch_jobs"),
    path("match/", JobMatchView.as_view(), name="job_match"),
    path("<int:id>/", JobDetailView.as_view(), name="job_detail"),
]