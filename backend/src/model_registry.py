import pickle

import pandas as pd
import mlflow
import mlflow.sklearn


def save_best_model(comparison_csv_path):
    df = pd.read_csv(comparison_csv_path)

    # Select best model using ROC-AUC (can justify this in exam)
    best_model_name = df.sort_values(
        by="roc_auc", ascending=False
    ).iloc[0]["model"]

    print(f"Best model selected: {best_model_name}")

    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(
        "Heart Disease Prediction"
    )

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"tags.mlflow.runName = '{best_model_name}'"
    )

    best_run = runs[0]
    model_uri = f"runs:/{best_run.info.run_id}/model"

    # Save as MLflow registered model
    result = mlflow.register_model(
        model_uri=model_uri,
        name="HeartDiseaseClassifier"
    )

    # Promote to staging
    client.transition_model_version_stage(
        name="HeartDiseaseClassifier",
        version=result.version,
        stage="staging",
        archive_existing_versions=True
    )

    # Load model and save as pickle
    model = mlflow.sklearn.load_model(model_uri)

    with open("exported_model/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Final model saved in MLflow Registry and as pickle")


if __name__ == "__main__":
    save_best_model("model_comparison.csv")
