# Added dummy message.
FROM python:3.12-slim

WORKDIR /app

# 1. Install system dependencies needed to build some python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .

# 2. Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ARG MLFLOW_TRACKING_URI
# ENV MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}

COPY . .

# # Download Production/Staging model at BUILD TIME
# RUN python - <<EOF
# import mlflow
# mlflow.set_tracking_uri("${MLFLOW_TRACKING_URI}")
# mlflow.artifacts.download_artifacts(
#     artifact_uri="models:/HeartDiseaseClassifier/Staging",
#     dst_path="exported_model"
# )
# EOF

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]