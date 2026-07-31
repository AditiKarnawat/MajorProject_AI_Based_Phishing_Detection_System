import numpy as np
from typing import Dict, Any, List, Tuple
from app.services.model_trainer import load_active_model
from app.services.feature_extraction import extract_url_features, extract_email_features

FEATURE_COLS = [
    "url_length", "domain_length", "dot_count", "hyphen_count", "at_count",
    "question_count", "equals_count", "slash_count", "digit_ratio", "has_ip",
    "is_https", "is_suspicious_tld", "subdomain_count", "domain_entropy",
    "keyword_count", "is_shortener"
]

def calculate_risk_level(risk_score: float) -> str:
    """Map numeric risk score (0-100) to risk level classification."""
    if risk_score < 20.0:
        return "Safe"
    elif risk_score < 45.0:
        return "Low Risk"
    elif risk_score < 70.0:
        return "Medium Risk"
    elif risk_score < 88.0:
        return "High Risk"
    else:
        return "Critical Threat"

def predict_url_phishing(url: str) -> Tuple[bool, float, float, str, Dict[str, Any], List[Dict[str, str]]]:
    """
    Predict phishing probability for a given URL using ML model + rule engine.
    Returns: (is_phishing, risk_score, confidence_score, risk_level, features, indicators)
    """
    features, indicators = extract_url_features(url)
    
    # Load ML model
    model, meta = load_active_model()
    
    # Construct feature vector
    vector = [features.get(col, 0) for col in FEATURE_COLS]
    
    # ML Model Prediction Probability
    ml_prob = float(model.predict_proba([vector])[0][1])  # Class 1 = Phishing
    
    # Heuristic adjustment based on high-severity indicators
    high_count = sum(1 for ind in indicators if ind.get("severity") == "high")
    med_count = sum(1 for ind in indicators if ind.get("severity") == "medium")
    
    heuristic_boost = (high_count * 0.20) + (med_count * 0.10)
    combined_prob = min(1.0, max(0.0, (ml_prob * 0.6) + (heuristic_boost * 0.4)))
    
    # Final Risk Score (0 - 100)
    risk_score = round(combined_prob * 100.0, 1)
    
    # Confidence Score (0 - 100)
    distance_from_boundary = abs(combined_prob - 0.5) * 2.0
    confidence_score = round(min(99.0, max(65.0, 70.0 + (distance_from_boundary * 25.0) + (len(indicators) * 1.5))), 1)
    
    is_phishing = risk_score >= 50.0
    risk_level = calculate_risk_level(risk_score)

    return is_phishing, risk_score, confidence_score, risk_level, features, indicators


def predict_email_phishing(body: str, subject: str = "", headers: str = "") -> Tuple[bool, float, float, str, Dict[str, Any], List[Dict[str, str]]]:
    """
    Predict phishing risk for Email text & headers.
    """
    features, indicators = extract_email_features(body, subject, headers)
    
    # Base heuristic probabilities
    prob = 0.05
    
    if features["urgent_keyword_count"] > 0:
        prob += min(0.45, features["urgent_keyword_count"] * 0.20)
    if features["ip_url_count"] > 0:
        prob += 0.40
    if features["has_script_tags"] or features["has_form_tag"]:
        prob += 0.35
    if features["header_anomaly"]:
        prob += 0.35
    if features["url_count"] >= 3:
        prob += 0.20

    combined_prob = min(1.0, max(0.0, prob))
    risk_score = round(combined_prob * 100.0, 1)
    
    # If no indicators and length is normal, safe
    if not indicators and features["body_length"] > 10:
        risk_score = min(15.0, risk_score)
        combined_prob = risk_score / 100.0
        
    confidence_score = round(min(98.0, max(72.0, 75.0 + (len(indicators) * 4.0))), 1)
    is_phishing = risk_score >= 50.0
    risk_level = calculate_risk_level(risk_score)

    return is_phishing, risk_score, confidence_score, risk_level, features, indicators
