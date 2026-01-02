from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from .services import fetch_remoteok_jobs, fetch_careerjet_jobs
from .services import fetch_remoteok_jobs
from .serializers import JobSerializer
from resumes.models import Resume
from jobs.models import Job
from jobs.matching import calculate_match

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

class JobMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get latest resume
        resume = Resume.objects.filter(user=user).last()
        if not resume:
            return Response({"error": "No resume uploaded"}, status=400)

        user_skills = resume.skills
        results = []

        for job in Job.objects.all():
            score = calculate_match(user_skills, job.skills)

            results.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "match_score": score
            })

        # Sort jobs by match score
        results = sorted(results, key=lambda x: x["match_score"], reverse=True)

        return Response(results)
