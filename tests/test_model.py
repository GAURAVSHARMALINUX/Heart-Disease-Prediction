from fastapi.testclient import TestClient
from api.app import app
import os

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Heart Disease Prediction API"}

def test_predict():
    # Make sure model is trained
    if not os.path.exists("models/model.joblib"):
        os.system("python src/train.py")
        
    sample_data = {
        "age": 63.0,
        "sex": 1,
        "cp": 3,
        "trestbps": 145.0,
        "chol": 233.0,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150.0,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0.0,
        "thal": 1
    }
    
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert "confidence" in json_data
