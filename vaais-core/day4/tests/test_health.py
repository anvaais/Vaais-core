from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_response():
    # 1. Act: Call your health endpoint (use "/" or "/health" depending on your main.py)
    response = client.get("/")
    
    # 2. Assert: Check status code 200 and exact JSON shape
    assert response.status_code == 200
    assert response.json() == {"message": "Lead Extraction API is running"}