import os, io, pdfplumber, pytesseract
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi import Body
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Resume
from docx import Document
from PIL import Image
from ..utils.ai_parser import analyze_resume
from ..utils.auth import verify_token

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])

ALLOWED_EXT = {".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))

def extract_text(file: UploadFile) -> str:
    name = file.filename.lower()
    if name.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text
    elif name.endswith(".docx"):
        doc = Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".txt"):
        return file.file.read().decode("utf-8", errors="ignore")
    elif any(name.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
        image = Image.open(file.file)
        return pytesseract.image_to_string(image)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

@router.post("/upload", dependencies=[Depends(verify_token)])
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Invalid file format")
    if file.size and file.size > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        text = extract_text(file)
        ai_data = analyze_resume(text)

        resume = Resume(
           file_name=file.filename,
           file_type=ext,
           file_size=file.size or 0,
           raw_text=text[:50000],
           ai_enhancements=ai_data
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return {
            "id": resume.id,
            "file_name": resume.file_name,
            "message": "File processed and stored successfully",
            "preview": text[:300] + ("..." if len(text) > 300 else "")
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
    
@router.get("/{resume_id}")
def get_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {
        "id": resume.id,
        "file_name": resume.file_name,
        "uploaded_at": resume.uploaded_at,
        "ai_enhancements": resume.ai_enhancements
    }

@router.post("/{id}/match")
def match_resume(id: str, job_description: dict = Body(...), db: Session = Depends(get_db)):
    from ..utils.ai_parser import match_resume_with_job

    resume = db.query(models.Resume).filter(models.Resume.id == id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    parsed_data = resume.structured_data or {}

    result = match_resume_with_job(parsed_data, job_description)

    return {
        "resumeId": id,
        "jobTitle": job_description.get("title"),
        "company": job_description.get("company", "N/A"),
        "matchingResults": result
    }
    
@router.get("/analytics/{id}", dependencies=[Depends(verify_token)])
def analyze_resume(id: str, db: Session = Depends(get_db)):
    from ..utils.ai_parser import analyze_resume_quality

    resume = db.query(models.Resume).filter(models.Resume.id == id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    parsed_data = resume.structured_data or {}
    result = analyze_resume_quality(parsed_data)

    return {
        "resumeId": id,
        "fileName": resume.file_name,
        "analysis": result
    }
