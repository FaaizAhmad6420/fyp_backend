from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from pdfplumber import open as pdf_open
import docx

# Create your views here.

# Simple skill list
SKILLS = ["python", "django", "react", "javascript", "sql", "html", "css"]

class ResumeUploadView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def get_queryset(self):
        # Each user only sees their own resumes
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the user automatically
        resume = serializer.save(user=self.request.user)

        # Parse file to extract text
        file_path = resume.file.path
        text = ""

        if file_path.endswith(".pdf"):
            with pdf_open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        # Save extracted text
        resume.extracted_text = text.lower()

        # Extract skills
        resume.skills = [skill for skill in SKILLS if skill in text.lower()]
        resume.save()
