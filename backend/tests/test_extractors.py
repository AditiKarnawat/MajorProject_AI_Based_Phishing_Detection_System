from app.services.feature_extraction import extract_url_features, extract_email_features

def test_extract_url_features_suspicious():
    phish_url = "http://192.168.1.1/paypal-security-update-verify-account.login.php?user=123"
    features, indicators = extract_url_features(phish_url)
    
    assert features["has_ip"] == 1
    assert features["is_https"] == 0
    assert features["keyword_count"] >= 2
    assert len(indicators) >= 2

def test_extract_url_features_clean():
    clean_url = "https://www.example.org"
    features, indicators = extract_url_features(clean_url)
    
    assert features["has_ip"] == 0
    assert features["is_https"] == 1
    assert features["keyword_count"] == 0

def test_extract_email_features():
    email_body = "URGENT! Your bank account is suspended. Click here to verify password immediately!"
    features, indicators = extract_email_features(email_body, subject="Account Alert")
    
    assert features["urgent_keyword_count"] >= 2
    assert len(indicators) >= 1
