# Heart Disease Prediction: End-to-End MLOps Solution

[![CI/CD Pipeline](https://github.com/2024ab05112/heart-disease-app/actions/workflows/deploy.yml/badge.svg)](https://github.com/2024ab05112/heart-disease-app/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready machine learning system for heart disease risk prediction, featuring automated CI/CD, experiment tracking with MLflow, and scalable deployment on Azure Kubernetes Service (AKS).

## Live Access
All services are routed via a unified Nginx Ingress Controller:
- **Web Application:** [Frontend UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/)
- **API Documentation:** [Swagger UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/api/docs)
- **Monitoring:** [Grafana Dashboard](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/grafana/) | [Prometheus UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/prometheus/)

---

## Official Project Documentation
For the complete end-to-end report covering EDA, model details, architecture, and CI/CD workflows, please refer to:
- [**Project Documentation (Word)**](docs/Project_Documentation.docx)
- [**Video Walkthrough / Demo**](https://drive.google.com/file/d/1EAkUQg3R94hodZxZxqRHMX2v1R3LgmU4/view)
- [**Technical Wiki**](https://github.com/2024ab05112/heart-disease-app/wiki)

---

## System Architecture
The system utilizes a unified microservices architecture routed via a high-performance Nginx Ingress Controller.

```mermaid
graph TD
    User((User)) -->|Single IP| Ingress[Nginx Ingress]
    Ingress -->|/| Frontend[Frontend Web]
    Ingress -->|/api| Backend[Backend API]
    Ingress -->|/grafana| Grafana[Grafana]
    Ingress -->|/prometheus| Prometheus[Prometheus]
    
    Frontend -->|Internal Comms| Backend
    Backend -->|Metrics| Prometheus
    Prometheus -->|DB Query| Grafana
```

---

## Quick Start (Local Setup)

The easiest way to run the entire stack locally is via Docker Compose.

### Execution
```bash
# Build and start all services
docker-compose up --build
```
The application will be available at http://localhost.

---

## CI/CD Workflow
The project follows a robust automation lifecycle via GitHub Actions:
1. **Validation:** Automated linting and unit tests.
2. **Containerization:** Concurrent Docker builds.
3. **Auto-Infra:** Automatic AKS cluster management and Ingress installation.
4. **Deployment:** Dynamic DNS mapping and rollout to Azure.

---
*Developed as part of the MLOps Assignment*