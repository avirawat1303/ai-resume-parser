import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

def analyze_resume(resume_text: str):
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)

    summary = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "summary_preview": " ".join(resume_text.split()[:50])
    }

    return summary


def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:
        if len(line.split()) in [2, 3] and line[0].isupper():
            return line.strip()
    return "Unknown"


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"


def extract_phone(text):
    match = re.search(r'\+?\d[\d\-\s]{8,}\d', text)
    return match.group(0) if match else "Not found"


def extract_skills(text):
    common_skills = [
        "python", "java", "c++", "sql", "html", "css", "javascript",
        "react", "node", "machine learning", "data analysis",
        "flask", "django", "tensorflow", "pytorch", "communication",
        "leadership", "problem solving"
    ]
    found = [s for s in common_skills if s.lower() in text.lower()]
    return list(set(found)) or ["None found"]


def calculate_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(float(similarity * 100), 2)


def match_resume_with_job(resume_data: dict, job_description: dict):
    resume_text = " ".join([
        resume_data.get("summary_preview", ""),
        " ".join(resume_data.get("skills", []))
    ]).lower()

    job_text = (
        f"{job_description.get('title', '')} "
        f"{job_description.get('description', '')} "
        f"{' '.join(job_description.get('skills', {}).get('required', []))} "
        f"{' '.join(job_description.get('skills', {}).get('preferred', []))}"
    ).lower()

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])
    
    resume_skills = set(resume_data.get("skills", []))
    required = set(job_description.get("skills", {}).get("required", []))
    preferred = set(job_description.get("skills", {}).get("preferred", []))

    matched_required = resume_skills.intersection(required)
    matched_preferred = resume_skills.intersection(preferred)
    total_required = len(required) or 1
    total_preferred = len(preferred) or 1

    skill_score = (
        (len(matched_required) / total_required) * 0.7 +
        (len(matched_preferred) / total_preferred) * 0.3
    )
    overall_score = round((similarity * 0.6 + skill_score * 0.4) * 100, 2)
    return {
        "overallScore": overall_score,
        "similarity": round(similarity * 100, 2),
        "skillsMatch": {
            "requiredSkillsMatched": list(matched_required),
            "preferredSkillsMatched": list(matched_preferred),
            "missingRequired": list(required - matched_required),
            "missingPreferred": list(preferred - matched_preferred)
        },
        "recommendation": (
            "Strong Match" if overall_score > 75
            else "Moderate Match" if overall_score > 50
            else "Weak Match"
        )
    }

def analyze_resume_quality(resume_data: dict):

    text = resume_data.get("summary_preview", "").lower()
    word_count = len(re.findall(r"\w+", text))
    sentence_count = len(re.findall(r"[.!?]", text)) or 1
    avg_sentence_len = round(word_count / sentence_count, 2)

    common_keywords = ["python", "machine learning", "data", "project", "api", "flask", "sql"]
    keyword_freq = Counter({kw: text.count(kw) for kw in common_keywords})
    keyword_density = sum(keyword_freq.values()) / (word_count or 1)


    has_edu = bool(re.search(r"education|bachelor|master|degree", text))
    has_exp = bool(re.search(r"experience|internship|project", text))
    has_contact = bool(re.search(r"email|phone|linkedin", text))

    completeness = (
        (1 if has_edu else 0.3) +
        (1 if has_exp else 0.4) +
        (1 if has_contact else 0.3)
    ) / 3


    quality_score = round(((keyword_density * 200) + (completeness * 70)) * 100 / 140, 2)
    quality_score = min(quality_score, 100)

    suggestions = []
    if avg_sentence_len > 25:
        suggestions.append("Use shorter sentences for better readability.")
    if keyword_density < 0.01:
        suggestions.append("Add more role-specific technical keywords.")
    if not has_edu:
        suggestions.append("Include an Education section with degree and institution.")
    if not has_exp:
        suggestions.append("Add professional or project experience to strengthen the profile.")
    if not has_contact:
        suggestions.append("Include contact details like email, phone, or LinkedIn.")

    return {
        "qualityScore": quality_score,
        "keywordDensity": round(keyword_density, 3),
        "avgSentenceLength": avg_sentence_len,
        "completeness": round(completeness * 100, 2),
        "keywordsUsed": keyword_freq,
        "suggestions": suggestions or ["Looks strong overall!"],
    }
