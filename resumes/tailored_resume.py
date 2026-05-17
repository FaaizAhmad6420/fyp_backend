import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_tailored_resume(parsed_data, job_data):

    prompt = f"""
    You are an expert ATS resume optimizer.

    Rewrite and optimize the resume for this specific job.

    Resume Data:
    {json.dumps(parsed_data, indent=2)}

    Job Data:
    {json.dumps(job_data, indent=2)}

    TASKS:
    - Improve professional summary
    - Prioritize relevant skills
    - Add ATS keywords naturally
    - Highlight relevant experience
    - Keep professional formatting
    - Do NOT invent fake projects or fake experience
    - Return clean plain text only

    Format:
    Name
    Summary
    Skills
    Experience
    Education
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]
