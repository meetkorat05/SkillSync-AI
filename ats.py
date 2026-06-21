import re

def calculate_ats_score(resume_text):

    score = 0
    text = resume_text.lower()

    # Contact Information
    if re.search(r'\S+@\S+', resume_text):
        score += 10

    if re.search(r'\d{10}', resume_text):
        score += 10

    # Sections
    if "skills" in text:
        score += 10

    if "project" in text:
        score += 10

    if "education" in text:
        score += 10

    if "experience" in text:
        score += 10

    # Numbers / Achievements
    numbers = re.findall(
        r'\d+%|\d+\.\d+%|\d+',
        resume_text
    )

    if len(numbers) >= 5:
        score += 10

    elif len(numbers) >= 2:
        score += 5

    # Technical Skills
    tech_keywords = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "xgboost",
        "flask",
        "streamlit",
        "langchain",
        "langgraph",
        "pinecone",
        "rag",
        "api"
    ]

    found_skills = 0

    for skill in tech_keywords:

        if skill in text:
            found_skills += 1

    score += min(found_skills, 10)

    # Resume Length
    word_count = len(text.split())

    if 300 <= word_count <= 800:
        score += 10

    elif 200 <= word_count < 300:
        score += 5

    elif word_count > 1000:
        score -= 5

    # Missing Section Penalty
    required_sections = [
        "skills",
        "project",
        "education"
    ]

    missing = 0

    for section in required_sections:

        if section not in text:
            missing += 1

    score -= (missing * 5)

    return max(
        0,
        min(score, 100)
    )

def compare_skills(
        resume_skills,
        jd_skills):

    resume_set = set(
        [s.strip().lower().replace(".", "")
        for s in resume_skills.split(",")]
    )

    jd_set = set(
        [s.strip().lower().replace(".", "")
        for s in jd_skills.split(",")]
    )

    matched = resume_set.intersection(jd_set)

    missing = jd_set - resume_set

    score = (
        len(matched) /
        max(len(jd_set), 1)
    ) * 100

    return score, matched, missing