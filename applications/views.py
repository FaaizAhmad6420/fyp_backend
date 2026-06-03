from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from resumes.models import Resume
from jobs.models import Job

from rest_framework import generics
from .models import JobApplication
from .serializers import JobApplicationSerializer

from applications.cover_letter import generate_cover_letter
from applications.tailored_resume import generate_tailored_resume

from rest_framework.decorators import api_view, permission_classes

from io import BytesIO
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


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

        already_applied = JobApplication.objects.filter(
            user=user,
            job=job
        ).exists()

        if already_applied:
            return Response(
                {"error": "Already applied"},
                status=400
            )

        job_data = {
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "skills": job.skills,
        }

        try:

            cover_letter = generate_cover_letter(
                resume.parsed_data,
                job_data
            )

            tailored_resume = generate_tailored_resume(
                resume.parsed_data,
                job_data
            )

        except Exception as e:

            return Response(
                {
                    "error": f"AI generation failed: {str(e)}"
                },
                status=500
            )

        application = JobApplication.objects.create(
            user=user,
            resume=resume,
            job=job,
            cover_letter=cover_letter,
            tailored_resume=tailored_resume,
            ats_score=resume.ats_score,
            status="submitted"
        )

        serializer = JobApplicationSerializer(
            application
        )

        return Response(serializer.data)

class ApplicationListView(generics.ListAPIView):

    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

class UpdateApplicationView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        try:
            application = JobApplication.objects.get(
                id=pk,
                user=request.user
            )

            cover_letter = request.data.get("cover_letter")
            tailored_resume = request.data.get("tailored_resume")

            if cover_letter is not None:
                application.cover_letter = cover_letter

            if tailored_resume is not None:
                application.tailored_resume = tailored_resume

            application.save()

            return Response({
                "message": "Application updated successfully"
            })

        except JobApplication.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

class ApplicationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            application = JobApplication.objects.get(
                id=pk,
                user=request.user
            )

            serializer = JobApplicationSerializer(application)

            return Response(serializer.data)

        except JobApplication.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )

class DownloadCoverLetterPDF(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        application = JobApplication.objects.get(
            id=pk,
            user=request.user
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Cover Letter", styles["Title"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph(application.cover_letter or "", styles["Normal"]))

        doc.build(content)

        buffer.seek(0)

        return HttpResponse(
            buffer,
            content_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=cover_letter.pdf"
            }
        )

class DownloadResumePDF(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        application = JobApplication.objects.get(
            id=pk,
            user=request.user
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Tailored Resume", styles["Title"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph(application.tailored_resume or "", styles["Normal"]))

        doc.build(content)

        buffer.seek(0)

        return HttpResponse(
            buffer,
            content_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=resume.pdf"
            }
        )
