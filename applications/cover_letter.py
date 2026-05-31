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
    - Write a personalized cover letter
    - Mention the candidate's actual skills
    - Mention company name
    - Mention job title
    - Professional tone
    - Do not invent fake experience
    - Do not use placeholders
    - End with a professional closing
    - Return CLEAN HTML format
    - Use <h1>, <p>, <strong>, <ul><li>
    - NO markdown
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]