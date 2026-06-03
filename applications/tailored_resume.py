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
    - Optimize resume for ATS systems
    - Prioritize skills matching the job
    - Improve professional summary
    - Highlight relevant experience
    - Add important job keywords naturally
    - Keep all information truthful
    - Do not invent projects or experience
    - Return CLEAN HTML formatted resume
    - Use proper headings, sections, bullet lists
    - Return CLEAN HTML format
    - Use <h1>, <p>, <strong>, <ul><li>
    - NO markdown

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
