from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume
from .serializers import ResumeSerializer

from .parser import parse_resume
from .utils import extract_skills

from pdfplumber import open as pdf_open
import docx

# fallback skill list
SKILLS = ["python", "django", "react", "javascript", "sql", "html", "css"]

class ResumeUploadView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        file_path = resume.file.path

        # 🔹 Try apilayer first
        try:
            parsed_data = parse_resume(file_path)
            resume.parsed_data = parsed_data

            skills = extract_skills(parsed_data)
            resume.skills = skills

        except Exception:
            # 🔸 Fallback local parsing
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
