from django.urls import path
from .views import ApplicationListView, ApplyJobView

urlpatterns = [
    path("apply/", ApplyJobView.as_view(), name="apply_job"),
    path("history/", ApplicationListView.as_view(), name="application_history"),
]
