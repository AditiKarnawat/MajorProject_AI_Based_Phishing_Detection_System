import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.scan import ScanRecord
from app.schemas.scan import ScanResultResponse, ScanHistoryPaginated, ScanListItem
from app.services.gemini_explainer import build_fallback_explanation

router = APIRouter(prefix="/history", tags=["Scan History"])

@router.get("", response_model=ScanHistoryPaginated)
def get_scan_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    scan_type: Optional[str] = Query(None, description="Filter by type: url, email, website"),
    search: Optional[str] = Query(None, description="Search term in target input"),
    only_phishing: Optional[bool] = Query(None, description="Filter only phishing detections"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve filterable, paginated scan history log."""
    query = db.query(ScanRecord)

    if current_user:
        query = query.filter(ScanRecord.user_id == current_user.id)

    if scan_type:
        query = query.filter(ScanRecord.scan_type == scan_type.lower())

    if only_phishing is not None:
        query = query.filter(ScanRecord.is_phishing == only_phishing)

    if search:
        query = query.filter(ScanRecord.target_input.ilike(f"%{search}%"))

    total = query.count()
    offset = (page - 1) * limit
    records = query.order_by(ScanRecord.created_at.desc()).offset(offset).limit(limit).all()

    items = [ScanListItem.from_orm(r) for r in records]

    return ScanHistoryPaginated(
        total=total,
        page=page,
        limit=limit,
        items=items
    )


@router.get("/{scan_id}", response_model=ScanResultResponse)
def get_scan_detail(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Retrieve detailed scan record by ID."""
    record = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found")

    if current_user and record.user_id and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden to this scan record")

    explanation = None
    if record.ai_explanation:
        if isinstance(record.ai_explanation, str):
            try:
                explanation = json.loads(record.ai_explanation)
            except Exception:
                explanation = None
        else:
            explanation = record.ai_explanation

    if not explanation or not isinstance(explanation, dict):
        explanation = build_fallback_explanation(
            target_input=record.target_input,
            scan_type=record.scan_type,
            is_phishing=record.is_phishing,
            risk_score=record.risk_score,
            indicators=record.indicators or []
        )

    return ScanResultResponse(
        id=record.id,
        scan_type=record.scan_type,
        target_input=record.target_input,
        is_phishing=record.is_phishing,
        risk_score=record.risk_score,
        confidence_score=record.confidence_score,
        risk_level=record.risk_level,
        extracted_features=record.extracted_features or {},
        indicators=record.indicators or [],
        ai_explanation=explanation,
        created_at=record.created_at
    )


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan_record(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Delete a scan record from history."""
    record = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found")

    if current_user and record.user_id and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    db.delete(record)
    db.commit()
    return None
