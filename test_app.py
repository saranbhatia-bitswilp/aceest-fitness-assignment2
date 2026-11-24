from app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.json["status"] == "ok"

def test_programs():
    client = app.test_client()
    response = client.get("/programs")
    assert "fat-loss" in response.json["programs"]

def test_calories():
    client = app.test_client()
    response = client.post(
        "/calculate-calories",
        json={"weight_kg": 80, "program": "fat-loss"}
    )
    assert response.status_code == 200
    assert response.json["estimated_kcal"] == 1760

def test_invalid_weight():
    client = app.test_client()
    response = client.post(
        "/calculate-calories",
        json={"weight_kg": -5, "program": "fat-loss"}
    )
    assert response.status_code == 400
