import re

def anonymize_text(text: str):
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', "[EMAIL]", text)
    text = re.sub(r'\+?\d[\d\s\-]{7,}\d', "[PHONE]", text)
    text = re.sub(r'(linkedin\.com/in/\S+|github\.com/\S+)', "[LINK]", text)
    return text
