import re
import PyPDF2
from roles_db import ROLE_SKILLS
from project_db import ROLE_PROJECTS

# PDF TEXT
def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "
    return text

# CLEAN TEXT
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s+#.-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# DETECT SKILLS
def detect_skills(text, skills):
    found = []
    for skill in skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return sorted(list(set(found)))

# ROLE RANKINGS
def get_role_rankings(text):
    results = []
    for role, skills in ROLE_SKILLS.items():
        matched = detect_skills(text, skills)
        score = round(
            (len(matched) / len(skills)) * 100)
        results.append((role, score))
    results.sort(
        key=lambda x: x[1],
        reverse=True)
    return results[:5]

# TARGET ROLE ANALYSIS
def analyze_target_role(text, role):
    skills = ROLE_SKILLS[role]
    matched = detect_skills(text, skills)
    missing = list(
        set(skills) - set(matched))
    score = round(
        (len(matched) / len(skills)) * 100)
    projects = ROLE_PROJECTS[role]
    roadmap = []
    for skill in missing[:5]:
        roadmap.append(
            f"Learn {skill.title()} this week")
    roadmap.append(
        "Build 2 projects for portfolio")
    roadmap.append(
        "Update resume with metrics")
    return {
        "score": score,
        "matched": matched,
        "missing": missing[:10],
        "projects": projects,
        "roadmap": roadmap
    }