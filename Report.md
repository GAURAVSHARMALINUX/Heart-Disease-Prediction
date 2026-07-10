# MLOps Assignment 01: Comprehensive Project Report

## Executive Summary
This report outlines the end-to-end design, development, and deployment of a machine learning classifier aimed at predicting heart disease using the UCI Heart Disease dataset. The project demonstrates a production-grade MLOps architecture encompassing data processing, model tracking, continuous integration, containerization, and Kubernetes deployment.

---

## 1. Introduction and Objectives
The primary objective of this project is to create a reproducible and scalable ML pipeline. The tasks span across Exploratory Data Analysis (EDA), Feature Engineering, Model Training, Experiment Tracking with MLflow, automated CI/CD pipelines via GitHub Actions, Containerization using Docker, and automated deployment configurations utilizing Helm Charts on Kubernetes.

---

## 2. Data Acquisition & Exploratory Data Analysis (EDA)
### 2.1 Data Source
The dataset (ID: 45) was automatically acquired from the UCI Machine Learning Repository via a custom python script utilizing the `ucimlrepo` library. The data consists of 14 features (including the target) covering vital clinical indicators like age, blood pressure, cholesterol levels, and fasting blood sugar.

### 2.2 EDA Findings
Extensive EDA was performed in a Jupyter environment (`notebooks/eda_and_modeling.ipynb`):
- **Class Balance:** The target variable (ranging originally from 0 to 4) was binarized (0: Absence, 1: Presence) to form a clear classification problem. The data is relatively balanced.
- **Correlations:** Features such as `cp` (chest pain type), `thalach` (maximum heart rate), and `exang` (exercise-induced angina) showed strong correlations with the target variable.
- **Distributions:** Histograms and KDE plots revealed that heart disease prevalence increases significantly with age and specific blood pressure thresholds.

---

## 3. Feature Engineering & Model Development
### 3.1 Preprocessing Pipeline
To guarantee reproducibility during inference, a strict `scikit-learn` pipeline (`ColumnTransformer`) was implemented in `src/data_preprocessing.py`:
- **Numerical Pipeline:** Handled via `SimpleImputer(strategy='median')` followed by `StandardScaler()`.
- **Categorical Pipeline:** Handled via `SimpleImputer(strategy='most_frequent')` followed by `OneHotEncoder(handle_unknown='ignore')`.

### 3.2 Model Training
Two baseline models were evaluated:
- **Logistic Regression:** Serves as a highly interpretable linear baseline.
- **Random Forest Classifier:** Serves as a robust non-linear ensemble method.

Both models were trained using an 80-20 stratified train-test split to preserve target distributions.

---

## 4. Experiment Tracking
**MLflow** was fully integrated into `src/train.py` to monitor and log experiments. 
For each run, the pipeline logs:
- **Parameters:** Model Type, hyperparameters.
- **Metrics:** Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
- **Artifacts:** The trained `scikit-learn` model itself.
This rigorous tracking ensures that no experiment context is lost and the best model is transparently selected and saved as `models/model.joblib`.

---

## 5. Model Serving and API Architecture
The selected model was deployed via a REST API utilizing **FastAPI**.
- The API exposes a `/predict` POST endpoint.
- It accepts a rigid JSON payload validated by **Pydantic** schemas.
- It transforms incoming data using the saved `preprocessor.joblib` and passes it to the `model.joblib`.
- **Monitoring Integration:** The application is instrumented using `prometheus_fastapi_instrumentator`, exposing a `/metrics` endpoint for real-time monitoring via Prometheus and Grafana.

---

## 6. Containerization
The FastAPI application is packaged using Docker.
- The `Dockerfile` uses a lightweight `python:3.9-slim` base image.
- It sequentially installs dependencies, executes the data download, runs the training script, and exposes port `8000`.
- The container ensures that the model executes flawlessly in an isolated environment, mitigating the "works on my machine" syndrome.

---

## 7. Kubernetes Deployment & Helm Charts
To scale the application, robust Kubernetes configurations were established:
- **Raw Manifests:** A standard `k8s/deployment.yaml` and `service.yaml` are available for quick deployments.
- **Helm Chart:** For production-grade package management, a custom Helm chart was built (`helm/heart-disease-api/`). This allows dynamic scaling, templated resource limits, and easy rollbacks. 
- The service is exposed via a `LoadBalancer` to ensure accessibility from external networks.

---

## 8. CI/CD Pipeline
An automated, multi-job GitHub Actions workflow (`.github/workflows/ci.yml`) acts as the backbone of the project's reliability:
1. **Code Quality:** Enforces syntax compliance using `flake8`.
2. **Model Training & Unit Tests:** Automatically downloads the data, trains the model, and runs the `pytest` suite (`tests/test_data.py`, `tests/test_model.py`) to validate model integrity and data schemas.
3. **Docker Build:** Reconstructs the Docker image to ensure the application remains buildable and deployable after every change.

An isolated secondary pipeline (`wiki-sync.yml`) exists exclusively to sync Markdown documentation to the GitHub Wiki.

---

## 9. Deployment Verification & Screenshots

The following endpoints were verified live after AKS deployment:

| Service | URL | Status |
|---------|-----|--------|
| Frontend Web App | `http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/` | Live |
| API Swagger Docs | `http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/api/docs` | Live |
| Grafana Dashboard | `http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/grafana/` | Live |
| Prometheus UI | `http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/prometheus/` | Live |

### Sample API Response (`/api/predict`):
```json
{
  "prediction": 1,
  "confidence": 0.87
}
```

### CI/CD Pipeline Execution
The full GitHub Actions pipeline (lint -> test -> train -> build -> deploy -> smoke-test) completes successfully on every push to `main`. Deployment screenshots are available in `docs/Screenshots/`.

---

## 10. Conclusion

This project successfully fulfills all the requirements of an end-to-end MLOps pipeline. The system transitions raw UCI Heart Disease CSV data into a monitored, containerized, and automatically tested Kubernetes-ready dual-service application.

Key achievements:
- Automated data ingestion and reproducible preprocessing pipeline
- Two ML models (Logistic Regression & Random Forest) with full MLflow experiment tracking
- FastAPI backend with `/api/predict` endpoint, confidence scores, and Prometheus metrics
- Django frontend for end-user interaction
- Multi-job GitHub Actions CI/CD with linting, unit tests, training, and AKS deployment
- Production-grade Prometheus + Grafana monitoring stack on Kubernetes
- Automated smoke testing after every deployment
