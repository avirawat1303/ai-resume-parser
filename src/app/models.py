from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base
import uuid

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    raw_text = Column(Text)
    ai_enhancements = Column(JSON) 
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
