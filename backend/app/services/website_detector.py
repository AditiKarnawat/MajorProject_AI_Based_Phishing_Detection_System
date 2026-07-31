import re
import urllib.parse
import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Tuple
from app.services.feature_extraction import extract_url_features

async def analyze_website_content(target_url: str) -> Tuple[Dict[str, Any], List[Dict[str, str]], Dict[str, Any]]:
    """
    Safely fetches target website HTML content, parses DOM for suspicious elements,
    and returns website-specific features, threat indicators, and raw metadata.
    """
    url_str = target_url.strip()
    if not url_str.startswith(("http://", "https://")):
        url_str = "https://" + url_str

    parsed_target = urllib.parse.urlparse(url_str)
    target_domain = parsed_target.netloc.split(":")[0].lower()

    # Base features from URL
    url_feats, url_indicators = extract_url_features(url_str)

    html_content = ""
    status_code = 0
    ssl_secure = True if parsed_target.scheme == "https" else False
    fetch_error = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 AIPhishingAuditor/1.0"
    }

    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True, verify=False) as client:
            resp = await client.get(url_str, headers=headers)
            status_code = resp.status_code
            html_content = resp.text
    except Exception as e:
        fetch_error = str(e)

    indicators = list(url_indicators)
    web_features = {
        "status_code": status_code,
        "ssl_secure": 1 if ssl_secure else 0,
        "page_size_bytes": len(html_content),
        "external_form_action_count": 0,
        "password_field_count": 0,
        "password_over_http": 0,
        "hidden_input_count": 0,
        "external_script_count": 0,
        "iframe_count": 0,
        "broken_link_count": 0,
        "brand_impersonation_detected": 0
    }

    if fetch_error or not html_content:
        indicators.append({
            "title": "Website Fetching Warning / Failure",
            "severity": "medium",
            "description": f"Could not retrieve web page content directly ({fetch_error or 'Empty Response'}). Analysis based on URL features."
        })
        return web_features, indicators, {"fetch_error": fetch_error}

    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Inspect Form tags
    forms = soup.find_all("form")
    for form in forms:
        action = form.get("action", "").strip()
        action_domain = ""
        if action:
            if action.startswith(("http://", "https://")):
                action_domain = urllib.parse.urlparse(action).netloc.split(":")[0].lower()
            elif not action.startswith(("#", "javascript:")):
                action_domain = target_domain
        
        # Check if form submits to external domain
        if action_domain and action_domain != target_domain and not action_domain.endswith("." + target_domain):
            web_features["external_form_action_count"] += 1
            
        # Check for password input fields
        pwd_inputs = form.find_all("input", {"type": "password"})
        if pwd_inputs:
            web_features["password_field_count"] += len(pwd_inputs)
            if not ssl_secure or (action.startswith("http://")):
                web_features["password_over_http"] = 1

    # 2. Hidden inputs
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    web_features["hidden_input_count"] = len(hidden_inputs)

    # 3. External Script Tags
    scripts = soup.find_all("script", src=True)
    for script in scripts:
        src = script.get("src", "")
        if src.startswith(("http://", "https://")):
            script_domain = urllib.parse.urlparse(src).netloc.split(":")[0].lower()
            if script_domain and script_domain != target_domain:
                web_features["external_script_count"] += 1

    # 4. IFrames
    iframes = soup.find_all("iframe")
    web_features["iframe_count"] = len(iframes)

    # 5. Broken/Empty Anchor Links
    anchors = soup.find_all("a")
    for a in anchors:
        href = a.get("href", "").strip()
        if href in ["#", "javascript:void(0)", "javascript:;", ""]:
            web_features["broken_link_count"] += 1

    # 6. Title and Brand Impersonation check
    title_tag = soup.find("title")
    page_title = title_tag.string.strip() if title_tag and title_tag.string else ""
    
    popular_brands = ["paypal", "microsoft", "google", "apple", "netflix", "amazon", "facebook", "instagram", "chase", "bank of america"]
    if page_title:
        lower_title = page_title.lower()
        for brand in popular_brands:
            if brand in lower_title and brand not in target_domain:
                web_features["brand_impersonation_detected"] = 1
                indicators.append({
                    "title": f"Potential Brand Impersonation ({brand.title()})",
                    "severity": "high",
                    "description": f"Page title contains '{page_title}' which references {brand.title()}, but domain '{target_domain}' does not match."
                })

    # Add HTML Indicators
    if web_features["external_form_action_count"] > 0:
        indicators.append({
            "title": "Cross-Domain Form Action Target",
            "severity": "high",
            "description": f"Detected {web_features['external_form_action_count']} form(s) submitting user data to external third-party domains."
        })

    if web_features["password_over_http"]:
        indicators.append({
            "title": "Insecure Password Transmission (HTTP)",
            "severity": "high",
            "description": "Page contains password input fields rendered without SSL/TLS encryption or submitting over plain HTTP."
        })

    if web_features["iframe_count"] > 0:
        indicators.append({
            "title": "Embedded IFrames Detected",
            "severity": "medium",
            "description": f"Found {web_features['iframe_count']} inline frame(s) that could be used for clickjacking or overlaid phishing forms."
        })

    if web_features["broken_link_count"] >= 5:
        indicators.append({
            "title": "High Number of Broken / Dummy Links",
            "severity": "medium",
            "description": f"Found {web_features['broken_link_count']} empty or dummy anchor links, commonly seen in cloned login templates."
        })

    meta_info = {
        "title": page_title,
        "status_code": status_code,
        "domain": target_domain,
        "forms_count": len(forms),
        "script_count": len(scripts)
    }

    return web_features, indicators, meta_info
