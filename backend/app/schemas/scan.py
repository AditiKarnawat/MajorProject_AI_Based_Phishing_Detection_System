from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class URLScanRequest(BaseModel):
    url: str = Field(..., description="URL string to analyze for phishing risks")

class EmailScanRequest(BaseModel):
    subject: Optional[str] = Field("", description="Email subject line")
    body: str = Field(..., description="Full email body content")
    headers: Optional[str] = Field("", description="Raw email headers if available")

class WebsiteScanRequest(BaseModel):
    url: str = Field(..., description="Target website URL to inspect live content")

class IndicatorItem(BaseModel):
    title: str
    severity: str  # 'high', 'medium', 'low', 'info'
    description: str

class AIExplanation(BaseModel):
    summary: str
    key_threats: List[str]
    technical_analysis: str
    recommendations: List[str]

class ScanResultResponse(BaseModel):
    id: Optional[int] = None
    scan_type: str
    target_input: str
    is_phishing: bool
    risk_score: float        # 0 - 100
    confidence_score: float  # 0 - 100
    risk_level: str          # Safe, Low Risk, Medium Risk, High Risk, Critical Threat
    extracted_features: Dict[str, Any]
    indicators: List[IndicatorItem]
    ai_explanation: AIExplanation
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScanListItem(BaseModel):
    id: int
    scan_type: str
    target_input: str
    is_phishing: bool
    risk_score: float
    confidence_score: float
    risk_level: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScanHistoryPaginated(BaseModel):
    total: int
    page: int
    limit: int
    items: List[ScanListItem]
