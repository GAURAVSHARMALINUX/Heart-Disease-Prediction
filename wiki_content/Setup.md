# Setup and Installation Guide

## Prerequisites

Before starting, ensure you have the following tools installed:
- **Docker**: For building container images.
- **Minikube**: Local Kubernetes cluster.
- **Kubectl**: Command-line tool for Kubernetes.
- **Python 3.9+**: For local development (optional).

## Quick Start (Kubernetes)

### 1. Start Minikube
Initialize your local Kubernetes cluster:
```bash
minikube start
```

### 2. Build Docker Images
You need to build the images locally or pull them if hosted. To build locally:

**Backend:**
```bash
docker build -t 2024ab05112/heart-disease-api:latest backend/
```

**Frontend:**
```bash
docker build -t 2024ab05112/heart-disease-frontend:latest frontend/
```

> **Note**: If using Minikube with the Docker driver, you might need to point your shell to Minikube's Docker daemon:
> `eval $(minikube -p minikube docker-env)`

### 3. Deploy to Kubernetes
Apply the configuration files located in the `k8s/` directory.

```bash
# Deploy Backend and Frontend
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/common/

# Deploy Monitoring (Optional)
kubectl apply -f k8s/monitoring/
```

### 4. Access the Application
Get the URL for the frontend service:
```bash
minikube service heart-disease-frontend-service --url
```
Open the provided URL in your browser to use the application.

## Local Development (Run without Docker)

**Backend:**
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run server: `uvicorn src.app:app --reload`.

**Frontend:**
1. Navigate to `frontend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run server: `python manage.py runserver`.
