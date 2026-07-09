# Welcome to the Heart Disease Prediction System Wiki

## Project Overview
This project is an end-to-end MLOps solution designed to predict the presence of heart disease in patients. It demonstrates a complete production pipeline, from model training to deployment on a Kubernetes cluster.

## Key Features
- **User-Friendly Interface**: A Django-based web application for easy data entry.
- **High-Performance Backend**: FastAPI microservice for real-time model inference.
- **Scalable Infrastructure**: Deployed on Kubernetes (Minikube) with auto-scaling capabilities.
- **Robust Monitoring**: Integrated Prometheus and Grafana for system observability.
- **Automated CI/CD**: GitHub Actions pipeline for continuous integration and deployment.

## Tech Stack
| Component | Technology |
|-----------|------------|
| **Frontend** | Django, HTML, CSS (Bootstrap) |
| **Backend** | FastAPI, Uvicorn, Python |
| **ML Model** | Scikit-Learn (Logistic Regression/Random Forest) |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (Minikube / Azure AKS) |
| **CI/CD** | GitHub Actions |

## Documentation Index
- **[[Setup and Installation|Setup]]**: Step-by-step guide to get the project running locally.
- **[[Cloud Deployment (AKS)|AKS_Deployment]]**: Production deployment guide using Azure and GitHub Actions.
- **[[Architecture Details|Architecture]]**: Deep dive into the system design and workflows.
- **[[API Documentation|API]]**: Details on the backend endpoints and usage.
- **[[Monitoring Guide|Monitoring]]**: How to use Prometheus and Grafana dashboards.
- **[Project Demonstration Video](https://drive.google.com/file/d/1EAkUQg3R94hodZxZxqRHMX2v1R3LgmU4/view)**: Complete video walkthrough of the system.
