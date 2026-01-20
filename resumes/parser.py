import requests
from django.conf import settings

APILAYER_URL = "https://api.apilayer.com/resume_parser/upload"

def parse_resume(file_path):
    headers = {
        "apikey": settings.APILAYER_API_KEY
    }

    with open(file_path, "rb") as f:
        response = requests.post(
            APILAYER_URL,
            headers=headers,
            files={"file": f}
        )

    if response.status_code != 200:
        raise Exception("apilayer parsing failed")

    return response.json()
