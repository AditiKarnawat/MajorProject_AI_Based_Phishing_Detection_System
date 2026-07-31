from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.scan import ScanRecord
from app.schemas.scan import (
    URLScanRequest, EmailScanRequest, WebsiteScanRequest, ScanResultResponse
)
from app.services.ml_service import predict_url_phishing, predict_email_phishing
from app.services.website_detector import analyze_website_content
from app.services.gemini_explainer import generate_ai_explanation

router = APIRouter(prefix="/scan", tags=["Phishing Scans"])

@router.post("/url", response_model=ScanResultResponse)
def scan_url(
    payload: URLScanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Analyze a URL target for phishing risks using ML models & Gemini AI."""
    url_target = payload.url.strip()
    if not url_target:
        raise HTTPException(status_code=400, detail="URL target cannot be empty")

    is_phishing, risk_score, confidence_score, risk_level, features, indicators = predict_url_phishing(url_target)
    
    ai_explanation = generate_ai_explanation(
        target_input=url_target,
        scan_type="URL",
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        indicators=indicators
    )

    scan_record = ScanRecord(
        user_id=current_user.id if current_user else None,
        scan_type="url",
        target_input=url_target,
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=features,
        indicators=indicators,
        ai_explanation=ai_explanation.get("summary", "")
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    return ScanResultResponse(
        id=scan_record.id,
        scan_type="url",
        target_input=url_target,
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=features,
        indicators=indicators,
        ai_explanation=ai_explanation,
        created_at=scan_record.created_at
    )


@router.post("/email", response_model=ScanResultResponse)
def scan_email(
    payload: EmailScanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Analyze email content & raw headers for phishing and social engineering triggers."""
    if not payload.body.strip():
        raise HTTPException(status_code=400, detail="Email body content cannot be empty")

    target_display = f"Subject: {payload.subject or 'No Subject'} | Body length: {len(payload.body)}"
    
    is_phishing, risk_score, confidence_score, risk_level, features, indicators = predict_email_phishing(
        body=payload.body,
        subject=payload.subject or "",
        headers=payload.headers or ""
    )

    ai_explanation = generate_ai_explanation(
        target_input=target_display,
        scan_type="Email",
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        indicators=indicators
    )

    scan_record = ScanRecord(
        user_id=current_user.id if current_user else None,
        scan_type="email",
        target_input=target_display,
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=features,
        indicators=indicators,
        ai_explanation=ai_explanation.get("summary", "")
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    return ScanResultResponse(
        id=scan_record.id,
        scan_type="email",
        target_input=target_display,
        is_phishing=is_phishing,
        risk_score=risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=features,
        indicators=indicators,
        ai_explanation=ai_explanation,
        created_at=scan_record.created_at
    )


@router.post("/website", response_model=ScanResultResponse)
async def scan_website(
    payload: WebsiteScanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Perform a deep live web page audit inspecting forms, links, scripts, and SSL security."""
    web_url = payload.url.strip()
    if not web_url:
        raise HTTPException(status_code=400, detail="Target website URL cannot be empty")

    web_features, indicators, meta_info = await analyze_website_content(web_url)
    
    # Calculate risk score based on website DOM inspection
    base_is_phish, base_risk, conf, rlevel, url_feats, _ = predict_url_phishing(web_url)
    
    # Add DOM level risks
    dom_boost = 0.0
    if web_features["external_form_action_count"] > 0:
        dom_boost += 30.0
    if web_features["password_over_http"]:
        dom_boost += 35.0
    if web_features["brand_impersonation_detected"]:
        dom_boost += 40.0
    if web_features["broken_link_count"] >= 5:
        dom_boost += 15.0

    final_risk_score = round(min(100.0, base_risk + dom_boost), 1)
    is_phishing = final_risk_score >= 50.0
    confidence_score = round(min(99.0, max(75.0, conf + (len(indicators) * 2.0))), 1)

    all_features = {**url_feats, **web_features}
    
    from app.services.ml_service import calculate_risk_level
    risk_level = calculate_risk_level(final_risk_score)

    ai_explanation = generate_ai_explanation(
        target_input=web_url,
        scan_type="Website",
        is_phishing=is_phishing,
        risk_score=final_risk_score,
        confidence_score=confidence_score,
        indicators=indicators
    )

    scan_record = ScanRecord(
        user_id=current_user.id if current_user else None,
        scan_type="website",
        target_input=web_url,
        is_phishing=is_phishing,
        risk_score=final_risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=all_features,
        indicators=indicators,
        ai_explanation=ai_explanation.get("summary", "")
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    return ScanResultResponse(
        id=scan_record.id,
        scan_type="website",
        target_input=web_url,
        is_phishing=is_phishing,
        risk_score=final_risk_score,
        confidence_score=confidence_score,
        risk_level=risk_level,
        extracted_features=all_features,
        indicators=indicators,
        ai_explanation=ai_explanation,
        created_at=scan_record.created_at
    )
