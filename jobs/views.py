from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import fetch_remoteok_jobs, fetch_careerjet_jobs
from .serializers import JobSerializer

# Create your views here.
class FetchJobsView(APIView):
    """
    Fetch jobs from APIs and return stored jobs.
    """
    def get(self, request):
        remoteok_jobs = fetch_remoteok_jobs()
        # careerjet_jobs = fetch_careerjet_jobs()
        # all_jobs = remoteok_jobs + careerjet_jobs
        all_jobs = remoteok_jobs

        serializer = JobSerializer(all_jobs, many=True)
        return Response({"jobs": serializer.data}, status=status.HTTP_200_OK)
