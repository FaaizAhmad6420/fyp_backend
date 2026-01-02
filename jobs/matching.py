def calculate_match(user_skills, job_skills):
    """
    Calculates match percentage between user skills and job skills
    """

    if not job_skills:
        return 0

    user_skills_set = set(skill.lower() for skill in user_skills)
    job_skills_set = set(skill.lower() for skill in job_skills)

    matched_skills = user_skills_set & job_skills_set

    match_percentage = (len(matched_skills) / len(job_skills_set)) * 100

    return round(match_percentage, 2)
