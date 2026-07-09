import os
import pandas as pd
from src.data_preprocessing import load_data, preprocess_and_split
from data.download_data import download_data

def test_data_download():
    download_data("data")
    assert os.path.exists("data/heart.csv"), "Data file was not downloaded."

def test_load_data():
    if not os.path.exists("data/heart.csv"):
        download_data("data")
    df = load_data("data/heart.csv")
    assert not df.empty, "Dataframe is empty."
    assert "num" in df.columns, "Target column 'num' is missing."
    assert set(df["num"].unique()).issubset({0, 1}), "Target column should be binarized."

def test_preprocess_and_split():
    df = load_data("data/heart.csv")
    X_train, X_test, y_train, y_test = preprocess_and_split(df, output_dir="models")
    
    assert X_train.shape[0] == len(y_train)
    assert X_test.shape[0] == len(y_test)
    assert X_train.shape[1] > 0
    assert os.path.exists("models/preprocessor.joblib"), "Preprocessor was not saved."
