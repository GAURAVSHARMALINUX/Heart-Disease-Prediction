import pandas as pd
from src.data_preprocessing import data_processing

def test_preprocessing_pipeline_runs():
    df = pd.DataFrame({
        "age": [63, 67, 67, 55, 60, 65, 58, 70, 62, 68],
        "sex": [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        "cp": [1, 4, 4, 2, 3, 1, 4, 2, 3, 1],
        "trestbps": [145, 160, 120, 140, 130, 125, 135, 150, 155, 128],
        "chol": [233, 286, 229, 250, 240, 220, 245, 260, 275, 235],
        "fbs": [1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        "restecg": [2, 2, 2, 1, 0, 2, 1, 2, 0, 1],
        "thalach": [150, 108, 129, 140, 125, 135, 145, 110, 120, 130],
        "exang": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
        "oldpeak": [2.3, 1.5, 2.6, 1.8, 2.0, 1.2, 2.5, 1.5, 2.2, 1.8],
        "slope": [3, 2, 2, 2, 3, 2, 1, 3, 2, 1],
        "ca": [0, 3, 2, 1, 2, 0, 3, 1, 2, 0],
        "thal": [6, 3, 7, 3, 6, 7, 3, 6, 3, 7],
        "target": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
    })

    preprocessor, X_train, X_test, y_train, y_test = data_processing(df)

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert len(y_train) + len(y_test) == len(df)



