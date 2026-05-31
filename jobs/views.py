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
class GetJobsView(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data}, status=status.HTTP_200_OK)
    
class JobDetailView(APIView):
    def get(self, request, id):
        job = Job.objects.get(id=id)
        serializer = JobSerializer(job)
        return Response(serializer.data)

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

        # Get latest resume (optional)
        resume = Resume.objects.filter(user=user).last()

        jobs = Job.objects.all()
        results = []

        # CASE 1: No resume → return jobs without scoring
        if not resume:
            for job in jobs:
                results.append({
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "url": job.url,
                })

            return Response(results)

        # CASE 2: Resume exists → calculate match score
        user_skills = resume.skills

        for job in jobs:
            score = calculate_match(user_skills, job.skills)

            results.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "match_score": score,
                "url": job.url,
            })

        # Sort only when score exists
        results = sorted(results, key=lambda x: x.get("match_score", 0), reverse=True)

        return Response(results)
