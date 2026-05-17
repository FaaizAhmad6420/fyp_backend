from django.urls import path
from .views import ApplyJobView

urlpatterns = [
    path("apply/", ApplyJobView.as_view(), name="apply_job"),
]