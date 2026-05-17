from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from resumes.models import Resume
from jobs.models import Job

from .models import JobApplication
from .serializers import JobApplicationSerializer


class ApplyJobView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        job_id = request.data.get("job_id")

        if not job_id:
            return Response(
                {"error": "job_id required"},
                status=400
            )

        # latest resume
        resume = Resume.objects.filter(
            user=user
        ).last()

        if not resume:
            return Response(
                {"error": "Upload resume first"},
                status=400
            )

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=404
            )

        # prevent duplicate
        already_applied = JobApplication.objects.filter(
            user=user,
            job=job
        ).exists()

        if already_applied:
            return Response(
                {"error": "Already applied"},
                status=400
            )

        application = JobApplication.objects.create(
            user=user,
            resume=resume,
            job=job,
            tailored_resume=resume.tailored_resume,
            cover_letter=resume.cover_letter,
            ats_score=resume.ats_score,
            status="submitted"
        )

        serializer = JobApplicationSerializer(
            application
        )

        return Response(serializer.data)