import os, io, pdfplumber, pytesseract
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from docx import Document
from PIL import Image
from ..db import get_db
from ..models import Resume
from ..utils.ai_parser import analyze_resume, match_resume_with_job, analyze_resume_quality
from ..utils.auth import verify_token
import uuid

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])

ALLOWED_EXT = {".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))

def extract_text(file: UploadFile) -> str:
    name = file.filename.lower()
    if name.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif name.endswith(".docx"):
        file.file.seek(0)
        doc = Document(io.BytesIO(file.file.read()))
        return "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".txt"):
        file.file.seek(0)
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

    try:
        text = extract_text(file)
        ai_data = analyze_resume(text)

        resume = Resume(
            file_name=file.filename,
            file_type=ext,
            file_size=len(text.encode('utf-8')),
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
def match_resume_route(id: str, job_description: dict = Body(...), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == id).first()
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
def analyze_resume_quality_route(id: str, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    parsed_data = resume.structured_data or {}
    result = analyze_resume_quality(parsed_data)

    return {
        "resumeId": id,
        "fileName": resume.file_name,
        "analysis": result
    }
