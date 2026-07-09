import os
import mlflow
import mlflow.sklearn
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from src.data_preprocessing import load_data, preprocess_and_split

def train_and_evaluate_model(X_train, X_test, y_train, y_test, model, model_name):
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        mlflow.log_param("model_type", model_name)
        if hasattr(model, "get_params"):
            mlflow.log_params(model.get_params())
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        if y_prob is not None:
            roc_auc = roc_auc_score(y_test, y_prob)
            mlflow.log_metric("roc_auc", roc_auc)
            print(f"{model_name} - Accuracy: {accuracy:.4f}, ROC-AUC: {roc_auc:.4f}")
        else:
            print(f"{model_name} - Accuracy: {accuracy:.4f}")
            
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        return model, accuracy

def main():
    mlflow.set_experiment("Heart_Disease_Prediction")
    
    print("Loading and preprocessing data...")
    df = load_data()
    X_train, X_test, y_train, y_test = preprocess_and_split(df)
    
    print("Training Logistic Regression...")
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr_model, lr_acc = train_and_evaluate_model(X_train, X_test, y_train, y_test, lr, "Logistic_Regression")
    
    print("Training Random Forest...")
    rf = RandomForestClassifier(random_state=42, n_estimators=100)
    rf_model, rf_acc = train_and_evaluate_model(X_train, X_test, y_train, y_test, rf, "Random_Forest")
    
    # Save the best model
    best_model = rf_model if rf_acc > lr_acc else lr_model
    joblib.dump(best_model, "models/model.joblib")
    print("Best model saved to models/model.joblib")

if __name__ == "__main__":
    main()
