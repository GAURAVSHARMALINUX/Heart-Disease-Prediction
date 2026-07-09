from pathlib import Path

import mlflow


def setup_mlflow():
    project_root = Path(__file__).resolve().parents[1]
    mlruns_path = project_root / "mlruns"

    mlflow.set_tracking_uri(f"file:///{mlruns_path}")
    mlflow.set_experiment("Heart Disease Prediction")
