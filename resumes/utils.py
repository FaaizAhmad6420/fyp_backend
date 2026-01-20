def extract_skills(parsed_data):
    skills = []

    try:
        skill_items = parsed_data.get("skills", [])
        for skill in skill_items:
            if isinstance(skill, dict):
                skills.append(skill.get("name").lower())
            elif isinstance(skill, str):
                skills.append(skill.lower())
    except Exception:
        pass

    return list(set(skills))
