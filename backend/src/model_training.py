import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import (
    cross_validate,
    StratifiedKFold,
    GridSearchCV,
    RandomizedSearchCV,
)

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


def tune_logistic_regression(preprocessor, X_train, y_train):
    """GridSearchCV for Logistic Regression."""
    base_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=1000, random_state=42))
    ])

    param_grid = {
        "model__C": [0.01, 0.1, 1, 10, 100],
        "model__solver": ["lbfgs", "liblinear"],
        "model__penalty": ["l2"],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    grid_search = GridSearchCV(
        base_pipeline,
        param_grid,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=0,
    )
    grid_search.fit(X_train, y_train)

    print(f"[LR] Best params: {grid_search.best_params_}")
    print(f"[LR] Best CV ROC-AUC: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search.best_params_


def tune_random_forest(preprocessor, X_train, y_train):
    """RandomizedSearchCV for Random Forest."""
    base_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestClassifier(random_state=42))
    ])

    param_dist = {
        "model__n_estimators": [50, 100, 200, 300],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2"],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    random_search = RandomizedSearchCV(
        base_pipeline,
        param_distributions=param_dist,
        n_iter=15,
        cv=cv,
        scoring="roc_auc",
        random_state=42,
        n_jobs=-1,
        verbose=0,
    )
    random_search.fit(X_train, y_train)

    print(f"[RF] Best params: {random_search.best_params_}")
    print(f"[RF] Best CV ROC-AUC: {random_search.best_score_:.4f}")

    return random_search.best_estimator_, random_search.best_params_


def train_models(preprocessor, X_train, X_test, y_train, y_test):
    tuners = {
        "logistic_regression": tune_logistic_regression,
        "random_forest": tune_random_forest,
    }

    comparison = []

    for name, tuner_fn in tuners.items():
        with mlflow.start_run(run_name=name):

            # Hyperparameter tuning
            best_pipeline, best_params = tuner_fn(
                preprocessor, X_train, y_train
            )

            # Log best hyperparameters
            mlflow.log_params(
                {k.replace("model__", ""): v for k, v in best_params.items()}
            )

            # Log the best tuned model
            mlflow.sklearn.log_model(best_pipeline, "model")

            # Cross-validation on tuned model
            cv_metrics = cross_validate_model(
                best_pipeline, X_train, y_train
            )

            # Final evaluation on held-out test set
            test_metrics = evaluate_and_log(
                best_pipeline, X_test, y_test, name
            )

            comparison.append({
                "model": name,
                **cv_metrics,
                **test_metrics,
            })

    # Save comparison table
    df = pd.DataFrame(comparison)
    df.to_csv("model_comparison.csv", index=False)
    mlflow.log_artifact("model_comparison.csv")
