from django.urls import path
from .views import ApplicationDetailView, ApplicationListView, ApplyJobView, UpdateApplicationView, DownloadCoverLetterPDF, DownloadResumePDF

urlpatterns = [
    path("apply/", ApplyJobView.as_view(), name="apply_job"),
    path("history/", ApplicationListView.as_view(), name="application_history"),
    path("update/<int:pk>/", UpdateApplicationView.as_view(), name="update_application"),
    path("detail/<int:pk>/", ApplicationDetailView.as_view(), name="application_detail"),
    path("download/cover/<int:pk>/", DownloadCoverLetterPDF.as_view()),
    path("download/resume/<int:pk>/", DownloadResumePDF.as_view()),
]
