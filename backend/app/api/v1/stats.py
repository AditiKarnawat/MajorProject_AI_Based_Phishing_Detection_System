from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.scan import ScanRecord
from app.schemas.stats import DashboardStatsResponse, RiskLevelCount, ScanTypeCount, TimelinePoint

router = APIRouter(prefix="/stats", tags=["Dashboard Analytics"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Generate executive dashboard KPIs, threat metrics, breakdown charts, and activity timeline."""
    query = db.query(ScanRecord)
    if current_user:
        query = query.filter(ScanRecord.user_id == current_user.id)

    total_scans = query.count()
    
    if total_scans == 0:
        return DashboardStatsResponse(
            total_scans=0,
            total_phishing_detected=0,
            total_safe_scans=0,
            phishing_ratio=0.0,
            average_risk_score=0.0,
            scans_by_type=[
                ScanTypeCount(name="URL Scans", value=0),
                ScanTypeCount(name="Email Scans", value=0),
                ScanTypeCount(name="Website Scans", value=0)
            ],
            scans_by_risk_level=[
                RiskLevelCount(name="Safe", value=0),
                RiskLevelCount(name="Low Risk", value=0),
                RiskLevelCount(name="Medium Risk", value=0),
                RiskLevelCount(name="High Risk", value=0),
                RiskLevelCount(name="Critical Threat", value=0)
            ],
            timeline=[],
            recent_threats=[]
        )

    phishing_count = query.filter(ScanRecord.is_phishing == True).count()
    safe_count = total_scans - phishing_count
    phishing_ratio = round((phishing_count / total_scans) * 100.0, 1)

    avg_risk = db.query(func.avg(ScanRecord.risk_score))
    if current_user:
        avg_risk = avg_risk.filter(ScanRecord.user_id == current_user.id)
    avg_risk_score = round(float(avg_risk.scalar() or 0.0), 1)

    # Scans by Type
    type_counts = db.query(
        ScanRecord.scan_type, func.count(ScanRecord.id)
    )
    if current_user:
        type_counts = type_counts.filter(ScanRecord.user_id == current_user.id)
    type_counts = type_counts.group_by(ScanRecord.scan_type).all()

    type_dict = {t.lower(): count for t, count in type_counts}
    scans_by_type = [
        ScanTypeCount(name="URL Scans", value=type_dict.get("url", 0)),
        ScanTypeCount(name="Email Scans", value=type_dict.get("email", 0)),
        ScanTypeCount(name="Website Scans", value=type_dict.get("website", 0)),
    ]

    # Scans by Risk Level
    risk_counts = db.query(
        ScanRecord.risk_level, func.count(ScanRecord.id)
    )
    if current_user:
        risk_counts = risk_counts.filter(ScanRecord.user_id == current_user.id)
    risk_counts = risk_counts.group_by(ScanRecord.risk_level).all()

    risk_dict = {r: count for r, count in risk_counts}
    scans_by_risk_level = [
        RiskLevelCount(name="Safe", value=risk_dict.get("Safe", 0)),
        RiskLevelCount(name="Low Risk", value=risk_dict.get("Low Risk", 0)),
        RiskLevelCount(name="Medium Risk", value=risk_dict.get("Medium Risk", 0)),
        RiskLevelCount(name="High Risk", value=risk_dict.get("High Risk", 0)),
        RiskLevelCount(name="Critical Threat", value=risk_dict.get("Critical Threat", 0)),
    ]

    # Timeline (Last 7 Days)
    today = datetime.utcnow().date()
    timeline = []
    for i in range(6, -1, -1):
        day_date = today - timedelta(days=i)
        day_start = datetime.combine(day_date, datetime.min.time())
        day_end = datetime.combine(day_date, datetime.max.time())
        
        day_query = db.query(ScanRecord).filter(
            ScanRecord.created_at >= day_start,
            ScanRecord.created_at <= day_end
        )
        if current_user:
            day_query = day_query.filter(ScanRecord.user_id == current_user.id)

        d_total = day_query.count()
        d_phish = day_query.filter(ScanRecord.is_phishing == True).count()
        d_safe = d_total - d_phish

        timeline.append(TimelinePoint(
            date=day_date.strftime("%b %d"),
            total=d_total,
            phishing=d_phish,
            safe=d_safe
        ))

    # Recent Threats (Recent 5 High/Critical scans)
    recent_query = db.query(ScanRecord).filter(
        ScanRecord.is_phishing == True
    )
    if current_user:
        recent_query = recent_query.filter(ScanRecord.user_id == current_user.id)
    
    recent_threats_records = recent_query.order_by(ScanRecord.created_at.desc()).limit(5).all()
    recent_threats = [
        {
            "id": r.id,
            "scan_type": r.scan_type,
            "target_input": r.target_input,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "created_at": r.created_at.isoformat() if r.created_at else datetime.utcnow().isoformat()
        } for r in recent_threats_records
    ]

    return DashboardStatsResponse(
        total_scans=total_scans,
        total_phishing_detected=phishing_count,
        total_safe_scans=safe_count,
        phishing_ratio=phishing_ratio,
        average_risk_score=avg_risk_score,
        scans_by_type=scans_by_type,
        scans_by_risk_level=scans_by_risk_level,
        timeline=timeline,
        recent_threats=recent_threats
    )
