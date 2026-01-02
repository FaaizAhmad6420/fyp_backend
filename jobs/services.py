import requests
from .models import Job

REMOTEOK_URL = "https://remoteok.com/api"  # Example API endpoint
CAREERJET_URL = "https://www.careerjet.com/api/job-search"  # Example endpoint

def fetch_remoteok_jobs():
    response = requests.get(REMOTEOK_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return []

    data = response.json()
    jobs = []

    for item in data:
        if 'position' not in item:
            continue  # skip invalid entries
        job, created = Job.objects.get_or_create(
            title=item.get("position"),
            company=item.get("company"),
            location=item.get("location") or "Remote",
            skills=item.get("tags", []),
            source="RemoteOK",
            defaults={
                "description": item.get("description") or "",
                "url": item.get("url") or "",
            }
        )
        jobs.append(job)
    return jobs

# def fetch_careerjet_jobs(keyword="developer", location="remote"):
#     params = {
#         "keywords": keyword,
#         "location": location,
#         "affid": "YOUR_AFFILIATE_ID",  # if required
#         "user_ip": "127.0.0.1",
#         "user_agent": "Mozilla/5.0",
#         "url": "http://127.0.0.1:8000",
#         "pagesize": 50
#     }
#     response = requests.get(CAREERJET_URL, params=params)
#     if response.status_code != 200:
#         return []

#     data = response.json()
#     jobs = []

#     for item in data.get("jobs", []):
#         job, created = Job.objects.get_or_create(
#             title=item.get("title"),
#             company=item.get("company"),
#             location=item.get("locations") or "Remote",
#             skills=[],  # CareerJet API may not provide skills directly
#             source="CareerJet",
#             defaults={
#                 "description": item.get("description") or "",
#                 "url": item.get("url") or "",
#             }
#         )
#         jobs.append(job)
#     return jobs
