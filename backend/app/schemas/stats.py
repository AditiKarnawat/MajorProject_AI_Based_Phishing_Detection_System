from typing import List, Dict, Any
from pydantic import BaseModel

class RiskLevelCount(BaseModel):
    name: str
    value: int

class ScanTypeCount(BaseModel):
    name: str
    value: int

class TimelinePoint(BaseModel):
    date: str
    total: int
    phishing: int
    safe: int

class DashboardStatsResponse(BaseModel):
    total_scans: int
    total_phishing_detected: int
    total_safe_scans: int
    phishing_ratio: float  # Percentage 0 - 100
    average_risk_score: float
    scans_by_type: List[ScanTypeCount]
    scans_by_risk_level: List[RiskLevelCount]
    timeline: List[TimelinePoint]
    recent_threats: List[Dict[str, Any]]
