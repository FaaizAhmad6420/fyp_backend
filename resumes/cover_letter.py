import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_cover_letter(resume_data, job_data):

    prompt = f"""
    You are a professional AI cover letter generator.

    Generate a SHORT professional cover letter.

    Candidate Resume:
    {json.dumps(resume_data, indent=2)}

    Job Details:
    {json.dumps(job_data, indent=2)}

    RULES:
    - Use professional tone
    - Mention relevant technical skills
    - Mention company name
    - Mention job title
    - Keep under 300 words
    - Do NOT invent fake experience
    - Do NOT use placeholders
    - Return plain text only
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]