import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"


def extract_json(text):
    """
    Extract valid JSON from AI response
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    return {}


def analyze_resume(parsed_data):

    prompt = f"""
    You are an ATS Resume Analyzer AI.

    Analyze this resume carefully.

    Resume Data:
    {json.dumps(parsed_data, indent=2)}

    IMPORTANT:
    Return ONLY valid JSON.
    No explanation.
    No markdown.
    No extra text.

    JSON format:

    {{
      "ats_score": 85,
      "career_domain": "Backend Development",
      "missing_skills": ["Docker", "AWS"],
      "strengths": [
        "Strong Django experience"
      ],
      "suggestions": [
        "Add measurable achievements"
      ]
    }}
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    ai_text = data["response"]

    return extract_json(ai_text)