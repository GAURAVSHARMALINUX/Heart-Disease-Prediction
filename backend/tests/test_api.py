from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "age": 50, "sex": 1, "cp": 0, "trestbps": 120,
        "chol": 240, "fbs": 0, "restecg": 1,
        "thalach": 150, "exang": 0, "oldpeak": 1.0,
        "slope": 1, "ca": 0, "thal": 2
    }

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 200
    assert "prediction" in response.json()
