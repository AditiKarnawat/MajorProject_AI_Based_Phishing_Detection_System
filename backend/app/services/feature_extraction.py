import re
import math
import urllib.parse
from typing import Dict, Any, List, Tuple
import tldextract

# Suspicious TLDs frequently used in phishing campaigns
SUSPICIOUS_TLDS = {
    "zip", "mov", "tk", "ml", "ga", "cf", "gq", "xyz", "top", "work",
    "click", "loan", "men", "guru", "asia", "club", "online", "site",
    "info", "ru", "cn", "fit", "rest", "surf", "casa", "beauty"
}

# Common URL shorteners
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly",
    "ow.ly", "tiny.cc", "rb.gy", "cutt.ly", "shorturl.at"
}

# Keywords commonly found in phishing URLs & emails
PHISHING_KEYWORDS = [
    "login", "signin", "verify", "verification", "account", "update",
    "banking", "secure", "security", "paypal", "appleid", "microsoft",
    "google", "netflix", "amazon", "confirm", "password", "credential",
    "support", "action-required", "billing", "wallet", "recovery", "auth"
]

# Email urgency & trigger words
URGENT_EMAIL_KEYWORDS = [
    "urgent", "immediately", "account suspended", "unusual activity",
    "action required", "click here", "wire transfer", "verify password",
    "security alert", "tax refund", "gift card", "ssn", "winner", "invoice",
    "limited time", "unauthorized login", "payment failed", "update payment"
]

def calculate_shannon_entropy(text: str) -> float:
    """Calculate Shannon Entropy (randomness) of a string."""
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return round(entropy, 4)

def extract_url_features(url: str) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """
    Extract 16+ numerical & categorical features from a URL for ML input,
    along with human-readable threat indicators.
    """
    url_str = url.strip()
    if not url_str.startswith(("http://", "https://")):
        url_str = "http://" + url_str

    parsed = urllib.parse.urlparse(url_str)
    domain_info = tldextract.extract(url_str)
    
    domain = domain_info.domain
    subdomain = domain_info.subdomain
    tld = domain_info.suffix.lower()
    fqdn = parsed.netloc.split(":")[0]

    # Feature 1: URL Length
    url_len = len(url_str)
    
    # Feature 2: Domain Length
    domain_len = len(domain)
    
    # Feature 3: Dot Count
    dot_count = url_str.count(".")
    
    # Feature 4: Hyphen Count in domain & path
    hyphen_count = url_str.count("-")
    
    # Feature 5: At (@) symbol count
    at_count = url_str.count("@")
    
    # Feature 6: Question (?) mark count
    question_count = url_str.count("?")
    
    # Feature 7: Equals (=) count
    equals_count = url_str.count("=")
    
    # Feature 8: Slash (/) count
    slash_count = url_str.count("/")
    
    # Feature 9: Digit count ratio
    digits = sum(c.isdigit() for c in url_str)
    digit_ratio = round(digits / max(1, url_len), 4)
    
    # Feature 10: Is IP address host
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    has_ip = 1 if re.match(ip_pattern, fqdn) else 0
    
    # Feature 11: Is HTTPS
    is_https = 1 if parsed.scheme == "https" else 0
    
    # Feature 12: Suspicious TLD
    is_suspicious_tld = 1 if tld in SUSPICIOUS_TLDS else 0
    
    # Feature 13: Subdomain count
    subdomains_list = [s for s in subdomain.split(".") if s]
    subdomain_count = len(subdomains_list)
    
    # Feature 14: Domain Shannon Entropy
    domain_entropy = calculate_shannon_entropy(fqdn)
    
    # Feature 15: Phishing Keyword Matches in URL
    lowered_url = url_str.lower()
    keyword_matches = [kw for kw in PHISHING_KEYWORDS if kw in lowered_url]
    keyword_count = len(keyword_matches)
    
    # Feature 16: URL Shortener Domain
    registered_domain = f"{domain_info.domain}.{domain_info.suffix}".lower()
    is_shortener = 1 if registered_domain in SHORTENER_DOMAINS or fqdn in SHORTENER_DOMAINS else 0

    features = {
        "url_length": url_len,
        "domain_length": domain_len,
        "dot_count": dot_count,
        "hyphen_count": hyphen_count,
        "at_count": at_count,
        "question_count": question_count,
        "equals_count": equals_count,
        "slash_count": slash_count,
        "digit_ratio": digit_ratio,
        "has_ip": has_ip,
        "is_https": is_https,
        "is_suspicious_tld": is_suspicious_tld,
        "subdomain_count": subdomain_count,
        "domain_entropy": domain_entropy,
        "keyword_count": keyword_count,
        "is_shortener": is_shortener
    }

    # Generate Human Indicators
    indicators = []
    if has_ip:
        indicators.append({
            "title": "IP Address used as Host",
            "severity": "high",
            "description": f"URL netloc '{fqdn}' uses a raw IP address instead of a domain name."
        })
    if is_suspicious_tld:
        indicators.append({
            "title": "High-Risk Top Level Domain (TLD)",
            "severity": "high",
            "description": f"The domain uses TLD '.{tld}', which is statistically associated with high phishing abuse."
        })
    if is_shortener:
        indicators.append({
            "title": "URL Shortening Service Detected",
            "severity": "medium",
            "description": "Shortened URLs obscure the actual destination domain."
        })
    if not is_https:
        indicators.append({
            "title": "Unencrypted HTTP Connection",
            "severity": "medium",
            "description": "The URL lacks SSL/TLS encryption (http://)."
        })
    if subdomain_count >= 3:
        indicators.append({
            "title": "Excessive Subdomains",
            "severity": "medium",
            "description": f"Found {subdomain_count} subdomains ({subdomain}), which can be used to spoof legitimate brand structures."
        })
    if domain_entropy > 4.2:
        indicators.append({
            "title": "High Domain Entropy (Randomness)",
            "severity": "medium",
            "description": f"Domain entropy score of {domain_entropy} indicates potential Domain Generation Algorithm (DGA) or random string."
        })
    if keyword_count > 0:
        indicators.append({
            "title": f"Phishing Keyword Matches ({keyword_count})",
            "severity": "high" if keyword_count >= 2 else "medium",
            "description": f"Detected security/banking keywords: {', '.join(keyword_matches[:4])}."
        })
    if url_len > 75:
        indicators.append({
            "title": "Abnormally Long URL",
            "severity": "low",
            "description": f"URL length is {url_len} characters, which may be attempting to hide the actual domain path."
        })

    return features, indicators


def extract_email_features(body: str, subject: str = "", headers: str = "") -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """
    Extract features from email subject, body, and raw headers.
    """
    combined_text = f"{subject} {body}".lower()
    
    # Feature 1: Body character length
    body_length = len(body)
    
    # Feature 2: Word count
    words = re.findall(r'\b\w+\b', combined_text)
    word_count = len(words)
    
    # Feature 3: Urgent / Phishing Keyword Matches
    matched_urgent = [kw for kw in URGENT_EMAIL_KEYWORDS if kw in combined_text]
    urgent_keyword_count = len(matched_urgent)
    
    # Feature 4: ALL CAPS Word Count
    body_words = re.findall(r'\b[A-Z]{3,}\b', body)
    all_caps_count = len(body_words)
    
    # Feature 5: Exclamation count
    exclamation_count = combined_text.count("!") + combined_text.count("?")
    
    # Feature 6: URL Count in Body
    urls_found = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
    url_count = len(urls_found)
    
    # Feature 7: IP URLs in Body
    ip_urls = [u for u in urls_found if re.search(r'https?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', u)]
    ip_url_count = len(ip_urls)
    
    # Feature 8: HTML Script Tag or Payload presence
    has_script_tags = 1 if re.search(r'<script.*?>|onload=|onclick=|javascript:', body, re.IGNORECASE) else 0
    
    # Feature 9: Form tag in email body
    has_form_tag = 1 if re.search(r'<form.*?>', body, re.IGNORECASE) else 0
    
    # Feature 10: Sender Header Anomaly (if headers provided)
    header_anomaly = 0
    if headers:
        from_match = re.search(r'From:\s*.*?<([^>]+)>|From:\s*([^\s\r\n]+)', headers, re.IGNORECASE)
        reply_match = re.search(r'Reply-To:\s*.*?<([^>]+)>|Reply-To:\s*([^\s\r\n]+)', headers, re.IGNORECASE)
        if from_match and reply_match:
            from_addr = from_match.group(1) or from_match.group(2)
            reply_addr = reply_match.group(1) or reply_match.group(2)
            from_domain = from_addr.split("@")[-1].lower() if "@" in from_addr else ""
            reply_domain = reply_addr.split("@")[-1].lower() if "@" in reply_addr else ""
            if from_domain and reply_domain and from_domain != reply_domain:
                header_anomaly = 1

    features = {
        "body_length": body_length,
        "word_count": word_count,
        "urgent_keyword_count": urgent_keyword_count,
        "all_caps_count": all_caps_count,
        "exclamation_count": exclamation_count,
        "url_count": url_count,
        "ip_url_count": ip_url_count,
        "has_script_tags": has_script_tags,
        "has_form_tag": has_form_tag,
        "header_anomaly": header_anomaly
    }

    indicators = []
    if urgent_keyword_count > 0:
        indicators.append({
            "title": "Urgent Action & Social Engineering Triggers",
            "severity": "high" if urgent_keyword_count >= 3 else "medium",
            "description": f"Detected high-urgency keywords: {', '.join(matched_urgent[:5])}."
        })
    if ip_url_count > 0:
        indicators.append({
            "title": "Direct IP Links in Email Body",
            "severity": "high",
            "description": f"Found {ip_url_count} link(s) pointing directly to raw IP addresses."
        })
    if header_anomaly:
        indicators.append({
            "title": "Sender Address Spoofing Anomaly",
            "severity": "high",
            "description": "Header 'From' domain differs from 'Reply-To' domain, suggesting email address spoofing."
        })
    if has_script_tags:
        indicators.append({
            "title": "Executable Code or Script Payload",
            "severity": "high",
            "description": "Email body contains active HTML `<script>` tags or JavaScript event handlers."
        })
    if has_form_tag:
        indicators.append({
            "title": "Embedded HTML Input Form",
            "severity": "medium",
            "description": "Email body contains an embedded `<form>` tag attempting to capture credentials inline."
        })
    if url_count >= 4:
        indicators.append({
            "title": "High Link Density",
            "severity": "medium",
            "description": f"Email body contains {url_count} embedded web URLs."
        })
    if all_caps_count >= 5:
        indicators.append({
            "title": "Aggressive Capitalization (Psychological Pressure)",
            "severity": "low",
            "description": f"Found {all_caps_count} words written in ALL CAPS."
        })

    return features, indicators
