def test_url_scan_endpoint(client):
    payload = {"url": "http://192.168.1.1/paypal-update-account-verification.login.php"}
    res = client.post("/api/v1/scan/url", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scan_type"] == "url"
    assert data["is_phishing"] is True
    assert data["risk_score"] > 50.0
    assert "ai_explanation" in data

def test_email_scan_endpoint(client):
    payload = {
        "subject": "Urgent Action Required: Account Suspension",
        "body": "Your bank account will be closed in 24 hours. Click http://10.0.0.1/verify to enter your password."
    }
    res = client.post("/api/v1/scan/email", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scan_type"] == "email"
    assert data["is_phishing"] is True

def test_stats_and_model_endpoints(client):
    stats_res = client.get("/api/v1/stats/dashboard")
    assert stats_res.status_code == 200
    stats_data = stats_res.json()
    assert "total_scans" in stats_data

    model_res = client.get("/api/v1/model/status")
    assert model_res.status_code == 200
    model_data = model_res.json()
    assert model_data["status"] == "online"
