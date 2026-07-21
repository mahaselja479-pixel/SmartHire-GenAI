def calculate_resume_score(parsed_resume):
    """
    Calculate a simple resume score based on available sections.
    """

    score = 0

    strengths = []
    weaknesses = []
    suggestions = []

    # Name
    if parsed_resume.get("name"):
        score += 10
        strengths.append("Name available")
    else:
        weaknesses.append("Missing name")

    # Email
    if parsed_resume.get("email"):
        score += 10
        strengths.append("Professional email")

    else:
        weaknesses.append("Email missing")

    # Phone
    if parsed_resume.get("phone"):
        score += 10
        strengths.append("Phone number available")

    else:
        weaknesses.append("Phone number missing")

    # Skills
    skills = parsed_resume.get("skills", [])

    if len(skills) >= 8:
        score += 25
        strengths.append("Strong technical skills")

    elif len(skills) >= 4:
        score += 15
        suggestions.append("Add more technical skills")

    else:
        weaknesses.append("Very few skills listed")

    # Projects
    projects = parsed_resume.get("projects", [])

    if len(projects) >= 2:
        score += 20
        strengths.append("Good project experience")

    else:
        suggestions.append("Add more projects")

    # Education
    if parsed_resume.get("education"):
        score += 15
        strengths.append("Education section present")

    else:
        weaknesses.append("Education missing")

    # Experience
    if parsed_resume.get("experience"):
        score += 10
        strengths.append("Experience included")

    else:
        suggestions.append("Add internship/work experience")

    return {
        "score": min(score, 100),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }