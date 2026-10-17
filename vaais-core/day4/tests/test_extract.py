from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

# Test 1: Basic valid extraction (200 OK) - SOLVED FOR EXAMPLE
def test_basic_extract():
    payload = {
        "text": "I am Anwar Ali and 3 travelers want to visit Skardu"
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Ye values main.py ke regex rules ke mutabiq exact match karti hain:
    assert data["status"] == "success"
    assert data["data"]["name"] == "Anwar Ali"
    assert data["data"]["travelers"] == 3
    assert data["data"]["location"] == "Skardu"


# Test 2: Absent traveler count - SOLVED FOR EXAMPLE
def test_absent_traveler_count():
    payload = {
        # Is sentence mein name aur city hai, magar travelers count nahi hai
        "text": "I am Anwar Ali and I want to visit Skardu"
    }
    response = client.post("/extract", json=payload)
    
    # Kyunki travelers optional hai, status 200 ayega aur travelers None hoga
    assert response.status_code == 200
    assert response.json()["data"]["travelers"] is None


# Test 3: Invalid field type / validation error (422 Unprocessable Entity) - YOUR TURN!
def test_invalid_field_type():
    payload = {
        # ANWAR ALI KI BARI: Niche "text": ke aage None ya "" (empty string) likhein
        # Misal ke taur par: "text": None
        "text": None  # <-- Aap isay None rehne dein ya "   " (khali spaces) kar ke test karein!
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 422


# Test 4: Malformed JSON syntax (422 Unprocessable Entity) - SOLVED
def test_malformed_json():
    broken_json = '{"text": "I am Anwar visiting Skardu"'  # Missing closing bracket }
    response = client.post(
        "/extract",
        content=broken_json,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422