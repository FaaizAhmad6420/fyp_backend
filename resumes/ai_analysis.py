import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_resume(parsed_data):
    """
    Sends resume data to Ollama AI
    and gets ATS analysis
    """

    prompt = f"""
    Analyze this resume data.

    Resume:
    {json.dumps(parsed_data, indent=2)}

    Return ONLY valid JSON in this format:

    {{
      "ats_score": number,
      "career_domain": "string",
      "missing_skills": ["skill1", "skill2"],
      "strengths": ["strength1", "strength2"],
      "suggestions": ["suggestion1", "suggestion2"]
    }}

    Do not add explanations.
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]