import pandas as pd
from src.data_ingestion import download_data
from src.data_preprocessing import *
from src.model_training import train_models
from src.mlflow_utils import setup_mlflow
from src.model_registry import save_best_model

def main():
    setup_mlflow()
    download_data()

    df = data_cleaning()
    data_visualization(df)

    preprocessor, X_train, X_test, y_train, y_test = data_processing(df)

    train_models(
        preprocessor,
        X_train,
        X_test,
        y_train,
        y_test
    )

    save_best_model("model_comparison.csv")

if __name__ == "__main__":
    main()
