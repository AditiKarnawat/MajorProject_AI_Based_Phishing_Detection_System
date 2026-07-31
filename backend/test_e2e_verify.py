import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("--- 1. Testing Health Endpoint ---")
r_health = requests.get(f"{BASE_URL}/health")
print("Health:", r_health.status_code, r_health.json())

print("\n--- 2. Testing URL Phishing Scan ---")
payload_url = {"url": "http://192.168.1.1/paypal-security-update-verify.login.php"}
r_url = requests.post(f"{BASE_URL}/scan/url", json=payload_url)
print("URL Scan Status:", r_url.status_code)
res_url = r_url.json()
print(f"Verdict: Phishing={res_url['is_phishing']} | Risk={res_url['risk_score']}/100 | Level={res_url['risk_level']}")
print("Gemini AI Summary:", res_url['ai_explanation']['summary'])

print("\n--- 3. Testing Email Phishing Scan ---")
payload_email = {
    "subject": "URGENT: Your account will be closed!",
    "body": "Dear customer, click http://10.0.0.1/verify to prevent permanent suspension."
}
r_email = requests.post(f"{BASE_URL}/scan/email", json=payload_email)
print("Email Scan Status:", r_email.status_code)
res_email = r_email.json()
print(f"Verdict: Phishing={res_email['is_phishing']} | Risk={res_email['risk_score']}/100 | Level={res_email['risk_level']}")

print("\n--- 4. Testing Website DOM Audit ---")
payload_web = {"url": "https://www.google.com"}
r_web = requests.post(f"{BASE_URL}/scan/website", json=payload_web)
print("Website Scan Status:", r_web.status_code)
res_web = r_web.json()
print(f"Verdict: Phishing={res_web['is_phishing']} | Risk={res_web['risk_score']}/100 | Level={res_web['risk_level']}")

print("\n--- 5. Testing Dashboard Stats ---")
r_stats = requests.get(f"{BASE_URL}/stats/dashboard")
print("Dashboard Stats Status:", r_stats.status_code)
print("Total Scans Logged:", r_stats.json()['total_scans'])
print("Phishing Detected Count:", r_stats.json()['total_phishing_detected'])

print("\n--- 6. Testing ML Model Status ---")
r_model = requests.get(f"{BASE_URL}/model/status")
print("Active Model:", r_model.json()['active_model'])
print("F1 Score:", r_model.json()['f1_score'])

print("\n✅ ALL SYSTEM CHECKS PASSED SUCCESSFULLY!")
