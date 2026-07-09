import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate, StratifiedKFold

from src.model_evaluate import evaluate_and_log


def cross_validate_model(pipeline, X, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"]
    )

    avg_scores = {
        f"cv_{metric}_mean": scores[f"test_{metric}"].mean()
        for metric in [
            "accuracy", "precision", "recall", "f1", "roc_auc"
        ]
    }

    mlflow.log_metrics(avg_scores)

    return avg_scores


def train_models(preprocessor, X_train, X_test, y_train, y_test):
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    }

    comparison = []

    for name, model in models.items():
        with mlflow.start_run(run_name=name):

            pipeline = Pipeline([
                ("preprocess", preprocessor),
                ("model", model)
            ])

            pipeline.fit(X_train, y_train)

            mlflow.sklearn.log_model(pipeline, "model")
            mlflow.log_params(model.get_params())

            # Cross-validation
            cv_metrics = cross_validate_model(pipeline, X_train, y_train)

            # Test evaluation
            test_metrics = evaluate_and_log(
                pipeline, X_test, y_test, name
            )

            comparison.append({
                "model": name,
                **cv_metrics,
                **test_metrics
            })

    # Save model comparison
    df = pd.DataFrame(comparison)
    df.to_csv("model_comparison.csv", index=False)
    mlflow.log_artifact("model_comparison.csv")
