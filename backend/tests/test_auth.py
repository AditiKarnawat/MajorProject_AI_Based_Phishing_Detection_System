def test_register_and_login(client):
    # Register new user
    reg_payload = {
        "full_name": "Test Security Officer",
        "email": "officer@security.org",
        "password": "SecretPassword123!"
    }
    response = client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "officer@security.org"

    # Duplicate registration should fail
    dup_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_res.status_code == 400

    # Login
    login_payload = {
        "email": "officer@security.org",
        "password": "SecretPassword123!"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data

    # Profile check with Bearer token
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "officer@security.org"
