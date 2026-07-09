# MLOps Assignment 01 - Project Report

## 1. Project Overview
This project demonstrates an end-to-end machine learning lifecycle (MLOps) using the UCI Heart Disease dataset. The objective is to build, track, containerize, and deploy a machine learning classifier to predict the presence of heart disease.

## 2. Setup and Installation
- A `requirements.txt` file is provided specifying all library versions.
- Running `python data/download_data.py` acquires the dataset directly from the UCI ML repository using `ucimlrepo`.

## 3. Exploratory Data Analysis (EDA) and Modeling Choices
- The `notebooks/eda_and_modeling.ipynb` notebook details the EDA, showcasing class distributions, correlation heatmaps, and age-related trends.
- **Preprocessing**: We used a `ColumnTransformer` with `SimpleImputer` and `StandardScaler` for numeric variables, and `OneHotEncoder` for categorical variables.
- **Modeling**: Logistic Regression and Random Forest models were trained. Random Forest demonstrated robust performance while tracking multiple metrics in MLflow.

## 4. Experiment Tracking
- MLflow was utilized to log metrics such as accuracy, precision, recall, F1-score, and ROC-AUC.
- Run tracking allows comparison of experiments, parameters, and logged artifacts (models).

## 5. CI/CD Pipeline
- GitHub Actions automatically trigger on push/pull requests to the `main` branch.
- The pipeline checks out the repository, installs dependencies, trains the model to confirm code execution, runs unit tests using `pytest`, and finally tests the Docker build process.

## 6. Architecture Diagram
```
[UCI ML Repo] --> (data/download_data.py) --> (data/heart.csv)
                                                    |
                                                    v
[MLflow Tracking] <-- (src/train.py) <--- (src/data_preprocessing.py)
                                                    |
                                                    v
                                            (models/model.joblib)
                                            (models/preprocessor.joblib)
                                                    |
                                                    v
[Users] <---> (FastAPI /predict endpoint) <--- [Docker Container] <--- [Kubernetes Deployment]
```

## 7. Containerization & Deployment
- The FastAPI application is containerized utilizing a `Dockerfile`.
- `k8s/deployment.yaml` exposes the containerized API locally (via Minikube or Docker Desktop Kubernetes) under a LoadBalancer service, effectively simulating production rollout.

## 8. API Monitoring Strategy
- Logging is incorporated inside the FastAPI app to track request status.
- Future expansions can integrate Prometheus metrics via a `/metrics` endpoint to visualize using Grafana.
