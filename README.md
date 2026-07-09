# Heart Disease Prediction - MLOps Assignment 01

This repository contains an end-to-end Machine Learning Operations (MLOps) pipeline for predicting heart disease based on the UCI Heart Disease dataset.

## Project Structure

- `data/`: Contains the download script and downloaded data.
- `src/`: Core Python modules for data preprocessing and model training.
- `notebooks/`: Jupyter notebook for EDA and prototyping.
- `api/`: FastAPI application for serving the model.
- `tests/`: Pytest test suite for testing data and model API.
- `models/`: Saved joblib models and MLflow artifacts.
- `k8s/`: Kubernetes manifests for deployment.
- `.github/workflows/`: CI/CD pipeline definition using GitHub Actions.

## Setup Instructions

1. **Install Requirements:**
   Ensure Python 3.9+ is installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Data:**
   ```bash
   python data/download_data.py
   ```

3. **Train Model:**
   ```bash
   python src/train.py
   ```

4. **Run API locally:**
   ```bash
   uvicorn api.app:app --host 0.0.0.0 --port 8000
   ```
   Access Swagger UI at `http://localhost:8000/docs`.

5. **Run Tests:**
   ```bash
   pytest tests/
   ```

## Docker and Deployment

**Build Docker Image:**
```bash
docker build -t heart-disease-api:latest .
```

**Run Container:**
```bash
docker run -p 8000:8000 heart-disease-api:latest
```

**Kubernetes Deployment (Standard Manifests):**
```bash
kubectl apply -f k8s/deployment.yaml
```

**Helm Chart Deployment (Recommended):**
```bash
helm upgrade --install heart-disease-api ./helm/heart-disease-api
```

## Monitoring
The API is instrumented with Prometheus. You can access the real-time metrics endpoint at:
```
http://localhost:8000/metrics
```
