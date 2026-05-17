from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume
from .serializers import ResumeSerializer

from .parser import parse_resume
from .utils import extract_skills

from pdfplumber import open as pdf_open
import docx

from .ai_analysis import analyze_resume
import json

from .cover_letter import generate_cover_letter
from jobs.models import Job

from rest_framework.views import APIView
from rest_framework.response import Response
from .tailored_resume import generate_tailored_resume

# fallback skill list
SKILLS = []

class ResumeUploadView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        file_path = resume.file.path

        try:
            parsed_data = parse_resume(file_path)
            resume.parsed_data = parsed_data

            # AI Resume Analysis
            try:
                try:
                    ai_data = analyze_resume(parsed_data)

                    resume.ai_analysis = ai_data
                    resume.ats_score = ai_data.get("ats_score", 0)

                except Exception as e:
                    resume.ai_analysis = {
                        "error": str(e)
                    }

                resume.ai_analysis = ai_data
                resume.ats_score = ai_data.get("ats_score", 0)

                # Generate AI Cover Letter
                try:
                    first_job = Job.objects.order_by("-id").first()

                    if first_job:
                        job_data = {
                            "title": first_job.title,
                            "company": first_job.company,
                            "description": first_job.description,
                            "skills": first_job.skills,
                        }

                        cover_letter = generate_cover_letter(
                            parsed_data,
                            job_data
                        )

                        resume.cover_letter = cover_letter

                except Exception as e:
                    print("Cover Letter Error:", e)

            except Exception as e:
                resume.ai_analysis = {
                    "error": str(e)
                }

            skills = extract_skills(parsed_data)
            resume.skills = skills

        except Exception:
            text = ""

            if file_path.endswith(".pdf"):
                with pdf_open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"

            elif file_path.endswith(".docx"):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"

            resume.extracted_text = text.lower()
            resume.skills = [s for s in SKILLS if s in text.lower()]

        resume.save()

class GenerateTailoredResumeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user
            )

            job = Job.objects.get(id=job_id)

            job_data = {
                "title": job.title,
                "company": job.company,
                "description": job.description,
                "skills": job.skills,
            }

            tailored_resume = generate_tailored_resume(
                resume.parsed_data,
                job_data
            )

            resume.tailored_resume = tailored_resume
            resume.save()

            return Response({
                "message": "Tailored resume generated",
                "tailored_resume": tailored_resume
            })

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=400)
