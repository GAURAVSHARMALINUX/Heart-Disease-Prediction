import logging
import time
from typing import Optional

import pandas as pd
import mlflow
import mlflow.sklearn
from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import generate_latest

from src.logging_config import setup_logging
from src.monitoring import REQUEST_COUNT, REQUEST_LATENCY


setup_logging()
logger = logging.getLogger(__name__)


# Load the trained model exported by the training pipeline
# Load the trained model exported by the training pipeline
model = mlflow.sklearn.load_model(model_uri="exported_model")

# Get root_path from environment variable (default to empty string)
# Note: With native /api prefix in routes, we might not strictly need root_path proxy logic, 
# but keeping it for Swagger UI doc generation if needed.
import os
root_path = os.getenv("ROOT_PATH", "")

app = FastAPI(
    title="Heart Disease Prediction API", 
    root_path=root_path,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Create a router with prefix /api
from fastapi import APIRouter
router = APIRouter(prefix="/api")

class PatientInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
    ).inc()

    REQUEST_LATENCY.observe(time.time() - start_time)
    return response


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@router.get("/")
def health_check():
    return "API is running"


@router.post("/predict")
def predict(data: PatientInput):
    logger.info("Prediction request received: %s", data)

    df = pd.DataFrame([data.dict()])
    prediction = int(model.predict(df)[0])

    confidence: Optional[float]
    try:
        proba = model.predict_proba(df)[0]
        confidence = float(proba[prediction])
    except Exception as exc:  # type: ignore
        logger.warning("Probability calculation failed: %s", exc)
        confidence = None

    logger.info("Prediction=%s, confidence=%s", prediction, confidence)
    return {"prediction": prediction, "confidence": confidence}

# Include the router in the app
app.include_router(router)

# Also expose health check on root for internal probes if needed (optional)
# But strictly speaking, our Ingress only sends /api to us.
# Liveness probe might check /api/
