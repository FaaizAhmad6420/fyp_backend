from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from xhtml2pdf import pisa
from django.http import HttpResponse

from resumes.models import Resume
from jobs.models import Job

from rest_framework import generics
from .models import JobApplication
from .serializers import JobApplicationSerializer

from applications.cover_letter import generate_cover_letter
from applications.tailored_resume import generate_tailored_resume

from rest_framework.decorators import api_view, permission_classes

from io import BytesIO


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from applications.pdf_generator import generate_pdf



PDF_STYLE = """
<style>

@page {
    size: A4;
    margin: 1.5cm;
}

body {
    font-family: Helvetica;
    font-size: 11pt;
    line-height: 1.5;
    word-wrap: break-word;
}

h1 {
    font-size: 22pt;
    margin-bottom: 10px;
    color: #1f2937;
}

h2 {
    font-size: 16pt;
    margin-top: 15px;
    margin-bottom: 8px;
    color: #374151;
    border-bottom: 1px solid #d1d5db;
}

h3 {
    font-size: 13pt;
    margin-top: 10px;
    margin-bottom: 5px;
}

p {
    margin-bottom: 8px;
}

ul {
    margin-left: 20px;
}

li {
    margin-bottom: 4px;
}

strong {
    font-weight: bold;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 8px;
}

blockquote {
    border-left: 4px solid #2563eb;
    padding-left: 10px;
    color: #555;
}

img {
    max-width: 100%;
}

pre {
    white-space: pre-wrap;
}

</style>
"""


def html_to_pdf(html):

    result = BytesIO()

    pdf_html = f"""
    <html>
        <head>
            {PDF_STYLE}
        </head>
        <body>
            {html}
        </body>
    </html>
    """

    pisa.CreatePDF(
        pdf_html,
        dest=result
    )

    result.seek(0)

    return result


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

        pdf = generate_pdf(
            application.cover_letter or ""
        )

        return HttpResponse(
            pdf,
            content_type="application/pdf",
            headers={
                "Content-Disposition":
                "attachment; filename=cover_letter.pdf"
            }
        )

class DownloadResumePDF(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        application = JobApplication.objects.get(
            id=pk,
            user=request.user
        )

        pdf = generate_pdf(
            application.tailored_resume or ""
        )

        return HttpResponse(
            pdf,
            content_type="application/pdf",
            headers={
                "Content-Disposition":
                "attachment; filename=resume.pdf"
            }
        )