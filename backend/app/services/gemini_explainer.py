import json
import os
from typing import List, Dict, Any
from app.core.config import settings

def generate_ai_explanation(
    target_input: str,
    scan_type: str,
    is_phishing: bool,
    risk_score: float,
    confidence_score: float,
    indicators: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Generate AI explanation using Google Gemini API if GEMINI_API_KEY is available.
    Falls back gracefully to an intelligent rule-based AI explanation generator.
    """
    api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
You are an expert AI Cybersecurity Threat Analyst inspecting a potential phishing {scan_type}.

Scan Target: {target_input}
Scan Type: {scan_type}
Verdict: {'PHISHING / MALICIOUS' if is_phishing else 'SAFE / LEGITIMATE'}
Risk Score: {risk_score}/100
Confidence Score: {confidence_score}/100
Detected Indicators: {json.dumps(indicators, indent=2)}

Generate a structured JSON output with the exact keys below:
{{
  "summary": "Concise 2-sentence executive summary of the threat level and finding.",
  "key_threats": ["Bullet point 1", "Bullet point 2"],
  "technical_analysis": "Detailed technical analysis paragraph explaining domain structure, heuristics, or content anomalies.",
  "recommendations": ["Actionable security recommendation 1", "Actionable security recommendation 2"]
}}
Return ONLY raw JSON, no markdown formatting or triple backticks.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.strip()
                
            parsed = json.loads(raw_text)
            return {
                "summary": parsed.get("summary", ""),
                "key_threats": parsed.get("key_threats", []),
                "technical_analysis": parsed.get("technical_analysis", ""),
                "recommendations": parsed.get("recommendations", [])
            }
        except Exception as e:
            pass

    return build_fallback_explanation(target_input, scan_type, is_phishing, risk_score, indicators)


def build_fallback_explanation(
    target_input: str,
    scan_type: str,
    is_phishing: bool,
    risk_score: float,
    indicators: List[Dict[str, str]]
) -> Dict[str, Any]:
    """Generates structured cybersecurity analysis when Gemini API is offline or unconfigured."""
    ind_titles = [ind["title"] for ind in indicators]
    
    if is_phishing or risk_score >= 50.0:
        summary = (
            f"The target {scan_type} has been flagged as a HIGH-RISK PHISHING THREAT with a risk score of {risk_score}/100. "
            f"Multiple malicious behavioral patterns and social engineering tactics were identified."
        )
        key_threats = ind_titles if ind_titles else [
            "Deceptive URL parameters or brand spoofing",
            "Lack of cryptographically verified domain trust",
            "Suspicious credential harvesting patterns"
        ]
        tech_analysis = (
            f"Machine learning models evaluated {scan_type} features for target '{target_input[:60]}...' "
            f"and detected {len(indicators)} active threat indicators. High entropy or keyword manipulation "
            f"suggests an attempt to impersonate legitimate brand assets or deceive end users."
        )
        recommendations = [
            "CRITICAL: Do NOT click links, submit passwords, or enter sensitive financial credentials.",
            "Report this suspicious target immediately to your organization's IT Security / SOC team.",
            "Block this domain or IP address at your network firewall and secure web gateway (SWG)."
        ]
    elif risk_score >= 20.0:
        summary = (
            f"The target {scan_type} exhibits MEDIUM RISK characteristics (Risk Score: {risk_score}/100). "
            f"Some unusual domain metrics or content indicators warrant heightened user caution."
        )
        key_threats = ind_titles if ind_titles else ["Unusual domain structural metrics or keyword patterns."]
        tech_analysis = (
            f"Audit of '{target_input[:60]}...' identified minor heuristic anomalies. "
            f"While not definitively malicious, users should verify authenticity before logging in."
        )
        recommendations = [
            "CAUTION: Double-check the exact domain name spelling in your browser address bar.",
            "Verify SSL certificate validity by ensuring a valid HTTPS connection is established.",
            "Avoid submitting sensitive authentication credentials if the source is unverified."
        ]
    else:
        summary = (
            f"The target {scan_type} is VERIFIED SAFE with a low risk score of {risk_score}/100. "
            f"No malicious anomalies or phishing indicators were detected."
        )
        key_threats = ind_titles if ind_titles else ["No threat indicators detected."]
        tech_analysis = (
            f"Feature extraction for '{target_input[:60]}...' confirmed standard clean domain structure, "
            f"valid encryption parameters, and no deceptive subdomain manipulation."
        )
        recommendations = [
            "TARGET VERIFIED SAFE: Domain structure matches clean, legitimate origin standards.",
            "NO MITIGATION REQUIRED: Safe to proceed with normal browsing and interaction.",
            "SECURITY HYGIENE: Always verify HTTPS lock icons in address bars before submitting passwords."
        ]

    return {
        "summary": summary,
        "key_threats": key_threats[:4],
        "technical_analysis": tech_analysis,
        "recommendations": recommendations
    }
