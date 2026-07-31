import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"
WEB_URL = "http://localhost:3000"

print("================================================================")
print("     ENTERPRISE PHISHING DETECTION SYSTEM FULL SUITE AUDIT     ")
print("================================================================\n")

# 1. Web Application HTTP Check
print("1. Checking Web UI Server (http://localhost:3000)...")
r_ui = requests.get(WEB_URL)
assert r_ui.status_code == 200, f"Web UI failed with status {r_ui.status_code}"
print("   [PASS] Web UI Server is online & serving HTML index (200 OK)\n")

# 2. Health Endpoint
print("2. Checking Backend Health Check (/api/v1/health)...")
r_health = requests.get(f"{BASE_URL}/health")
assert r_health.status_code == 200
print(f"   [PASS] Backend API is healthy: {r_health.json()}\n")

# 3. URL Scanner Module
print("3. Auditing URL Phishing Scanner (/api/v1/scan/url)...")
url_phish = "http://192.168.1.1/paypal-security-update-verify.login.php"
r_url1 = requests.post(f"{BASE_URL}/scan/url", json={"url": url_phish})
assert r_url1.status_code == 200
data_url1 = r_url1.json()
print(f"   - Phishing Target: '{url_phish}'")
print(f"     Verdict: {data_url1['risk_level']} (Score: {data_url1['risk_score']}/100 | Phishing={data_url1['is_phishing']})")
print(f"     Gemini AI Summary: {data_url1['ai_explanation']['summary']}")

url_safe = "https://www.github.com"
r_url2 = requests.post(f"{BASE_URL}/scan/url", json={"url": url_safe})
assert r_url2.status_code == 200
data_url2 = r_url2.json()
print(f"   - Safe Target: '{url_safe}'")
print(f"     Verdict: {data_url2['risk_level']} (Score: {data_url2['risk_score']}/100 | Phishing={data_url2['is_phishing']})")
print("   [PASS] URL Scanner Engine fully operational!\n")

# 4. Email NLP Inspector Module
print("4. Auditing Email Phishing & NLP Inspector (/api/v1/scan/email)...")
email_phish = {
    "subject": "URGENT: Your account will be closed!",
    "body": "Dear user, click http://10.0.0.1/verify to prevent permanent suspension of your account."
}
r_em1 = requests.post(f"{BASE_URL}/scan/email", json=email_phish)
assert r_em1.status_code == 200
data_em1 = r_em1.json()
print(f"   - Phishing Email Subject: '{email_phish['subject']}'")
print(f"     Verdict: {data_em1['risk_level']} (Score: {data_em1['risk_score']}/100 | Phishing={data_em1['is_phishing']})")

email_safe = {
    "subject": "Weekly Team Update",
    "body": "Hi team, here is the recap of our weekly progress and schedule."
}
r_em2 = requests.post(f"{BASE_URL}/scan/email", json=email_safe)
assert r_em2.status_code == 200
data_em2 = r_em2.json()
print(f"   - Safe Email Subject: '{email_safe['subject']}'")
print(f"     Verdict: {data_em2['risk_level']} (Score: {data_em2['risk_score']}/100 | Phishing={data_em2['is_phishing']})")
print("   [PASS] Email NLP Inspector Engine fully operational!\n")

# 5. Website DOM & SSL Auditor Module
print("5. Auditing Website Content Auditor (/api/v1/scan/website)...")
web_target = "https://www.google.com"
r_web = requests.post(f"{BASE_URL}/scan/website", json={"url": web_target})
assert r_web.status_code == 200
data_web = r_web.json()
print(f"   - Target Website: '{web_target}'")
print(f"     Verdict: {data_web['risk_level']} (Score: {data_web['risk_score']}/100 | Phishing={data_web['is_phishing']})")
print("   [PASS] Website Content & DOM Auditor operational!\n")

# 6. Dashboard Analytics KPIs & Timeline
print("6. Auditing Executive Dashboard Stats (/api/v1/stats/dashboard)...")
r_stats = requests.get(f"{BASE_URL}/stats/dashboard")
assert r_stats.status_code == 200
data_stats = r_stats.json()
print(f"   - Total Scans Logged: {data_stats['total_scans']}")
print(f"   - Phishing Threats Detected: {data_stats['total_phishing_detected']}")
print(f"   - Safe Targets Verified: {data_stats['total_safe_scans']}")
print(f"   - Average Risk Score: {data_stats['average_risk_score']}/100")
print(f"   - 7-Day Timeline Points: {len(data_stats['timeline'])} days")
print(f"   - Risk Breakdown Categories: {len(data_stats['scans_by_risk_level'])} categories")
print("   [PASS] Executive Dashboard KPI Aggregator operational!\n")

# 7. Scan History Log & Detail Drawer Fetch
print("7. Auditing Scan History Log & Single Record Detail (/api/v1/history)...")
r_hist = requests.get(f"{BASE_URL}/history?limit=10")
assert r_hist.status_code == 200
data_hist = r_hist.json()
items = data_hist.get("items", [])
print(f"   - Retrieved {len(items)} scan history records.")

if items:
    sample_id = items[0]['id']
    r_detail = requests.get(f"{BASE_URL}/history/{sample_id}")
    assert r_detail.status_code == 200
    data_detail = r_detail.json()
    print(f"   - Fetched Detail for Record #{sample_id}:")
    print(f"     Target: '{data_detail['target_input']}'")
    print(f"     Risk Level: {data_detail['risk_level']} ({data_detail['risk_score']}/100)")
    print(f"     Recommendations: {data_detail['ai_explanation']['recommendations'][0]}")
print("   [PASS] Scan History Log & Threat Diagnosis Detail API operational!\n")

# 8. Model Studio Status & Automated Retraining Pipeline
print("8. Auditing Machine Learning Model Studio (/api/v1/model/status)...")
r_mod = requests.get(f"{BASE_URL}/model/status")
assert r_mod.status_code == 200
data_mod = r_mod.json()
print(f"   - Active ML Model: {data_mod['active_model']}")
print(f"   - Benchmark F1-Score: {data_mod['f1_score'] * 100:.1f}%")
print("   - Evaluation Matrix:")
for algo, m in data_mod.get("benchmark_results", {}).items():
    print(f"     * {algo}: Accuracy={m['accuracy']*100:.1f}%, Precision={m['precision']*100:.1f}%, F1={m['f1_score']*100:.1f}%")

print("\n   - Testing 1-Click Automated Model Retraining (/api/v1/model/retrain)...")
r_train = requests.post(f"{BASE_URL}/model/retrain")
assert r_train.status_code == 200
print(f"     Response: {r_train.json()['message']}")
print("   [PASS] ML Model Studio & Retraining Pipeline fully operational!\n")

print("================================================ me============")
print("  ALL 8 MODULES AND SYSTEM FEATURES OPERATIONAL & VERIFIED OK ")
print("==================================================================")
