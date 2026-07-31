import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    scan_type = Column(String, nullable=False, index=True)  # 'url', 'email', 'website'
    target_input = Column(Text, nullable=False)
    
    is_phishing = Column(Boolean, nullable=False)
    risk_score = Column(Float, nullable=False)        # 0.0 - 100.0
    confidence_score = Column(Float, nullable=False)  # 0.0 - 100.0
    risk_level = Column(String, nullable=False)        # 'Safe', 'Low Risk', 'Medium Risk', 'High Risk', 'Critical Threat'
    
    extracted_features = Column(JSON, nullable=True)
    indicators = Column(JSON, nullable=True)          # List of suspicious flags
    ai_explanation = Column(Text, nullable=True)      # Detailed Gemini explanation or fallback
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user = relationship("User", back_populates="scans")
