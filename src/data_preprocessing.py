import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

def load_data(data_path="data/heart.csv"):
    df = pd.read_csv(data_path)
    # Binarize the target column (presence of heart disease)
    # Target in UCI dataset is often 0 for absence, and 1,2,3,4 for presence.
    if df['num'].max() > 1:
        df['num'] = df['num'].apply(lambda x: 1 if x > 0 else 0)
    return df

def get_preprocessor():
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    return preprocessor

def preprocess_and_split(df, output_dir="models"):
    X = df.drop('num', axis=1)
    y = df['num']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    preprocessor = get_preprocessor()
    
    # Fit and transform training data
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Save the preprocessor
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    joblib.dump(preprocessor, os.path.join(output_dir, 'preprocessor.joblib'))
    
    return X_train_processed, X_test_processed, y_train, y_test

if __name__ == "__main__":
    df = load_data()
    preprocess_and_split(df)
    print("Preprocessing completed and preprocessor saved.")
