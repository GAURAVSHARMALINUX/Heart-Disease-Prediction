import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')

TARGET = "target"
DATA_PATH_RAW = Path("data/raw")
DATA_PATH_CLEAN = Path("data/processed")
RAW_FILE = os.path.join(DATA_PATH_RAW, "processed.cleveland.data")
CLEAN_CSV = os.path.join(DATA_PATH_CLEAN, "heart_disease_cleaned.csv")


def data_cleaning():
    DATA_PATH_CLEAN.mkdir(parents=True, exist_ok=True)
    columns = [
        "age", "sex", "cp", "trestbps", "chol",
        "fbs", "restecg", "thalach", "exang",
        "oldpeak", "slope", "ca", "thal", "target"
    ]

    df = pd.read_csv(RAW_FILE, names=columns)

    # Replace missing value symbol
    df.replace("?", np.nan, inplace=True)

    # Convert all columns to numeric safely
    df = df.apply(pd.to_numeric, errors="coerce")

    # Handle missing values using median
    df.fillna(df.median(), inplace=True)

    # Convert target to binary (0 = No disease, 1 = Disease)
    df["target"] = df["target"].apply(
        lambda x: 1 if x > 0 else 0
    )

    # Save cleaned dataset as CSV
    df.to_csv(CLEAN_CSV, index=False)
    print(f"Cleaned dataset saved as CSV: {CLEAN_CSV}")

    print("Data first five rows")
    print(df.head())

    print("\nData shape:")
    print(df.shape)

    print("\nData info:")
    print(df.info())

    print("\nData description:")
    print(df.describe())

    print("\nData null values:")
    print(df.isnull().sum())

    return df


def data_visualization(df):
    plt.figure(figsize=(20, 10))
    sns.heatmap(df.corr(), annot=True)
    plt.savefig("reports/correlation_heatmap.png")
    plt.close()

    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.countplot(x="target", data=df)
    plt.title("Class Distribution (Heart Disease)")
    plt.xlabel("Target")
    plt.ylabel("Count")
    plt.savefig("reports/class_balance.png")
    plt.close()

    df.hist(
        bins=20,
        figsize=(12, 8),
        edgecolor="black"
    )
    plt.suptitle("Distribution of Numerical Features", fontsize=16)
    plt.savefig("reports/numerical_features_distribution.png")


def data_processing(df):
    X = df.drop(TARGET, axis=1)
    y = df[TARGET]

    num_features = [
        "age", "trestbps", "chol", "thalach", "oldpeak"
    ]

    cat_features = [
        "sex", "cp", "fbs", "restecg",
        "exang", "slope", "ca", "thal"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                cat_features
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    return preprocessor, X_train, X_test, y_train, y_test
