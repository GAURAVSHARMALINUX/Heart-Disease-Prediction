import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve,
)
import json
import matplotlib
matplotlib.use("Agg")


def evaluate_and_log(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
    }

    # ROC-AUC + ROC curve
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        metrics["roc_auc"] = roc_auc_score(y_test, y_prob)

        fpr, tpr, _ = roc_curve(y_test, y_prob)

        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC={metrics['roc_auc']:.2f}")
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve - {model_name}")
        plt.legend()
        roc_path = f"roc_curve_{model_name}.png"
        plt.savefig(roc_path)
        plt.close()

        mlflow.log_artifact(roc_path)

    # Log metrics
    mlflow.log_metrics(metrics)

    # Classification report
    report_txt = classification_report(y_test, y_pred)
    report_json = classification_report(y_test, y_pred, output_dict=True)

    txt_path = f"classification_report_{model_name}.txt"
    json_path = f"classification_report_{model_name}.json"

    with open(txt_path, "w") as f:
        f.write(report_txt)

    with open(json_path, "w") as f:
        json.dump(report_json, f, indent=4)

    mlflow.log_artifact(txt_path)
    mlflow.log_artifact(json_path)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix - {model_name}")

    cm_path = f"confusion_matrix_{model_name}.png"
    plt.savefig(cm_path)
    plt.close()

    mlflow.log_artifact(cm_path)

    return metrics
