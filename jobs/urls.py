from django.urls import path
from .views import FetchJobsView

urlpatterns = [
    path("fetch/", FetchJobsView.as_view(), name="fetch_jobs"),
]