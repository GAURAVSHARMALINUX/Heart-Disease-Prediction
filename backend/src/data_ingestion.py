import os
import urllib.request
from pathlib import Path

DATA_PATH = Path("data/raw")


def download_data():
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    url += "heart-disease/processed.cleveland.data"

    raw_file = os.path.join(DATA_PATH, "processed.cleveland.data")

    if not os.path.exists(raw_file):
        urllib.request.urlretrieve(url, raw_file)
        print("Dataset downloaded from UCI repository")
    else:
        print("Dataset already exists locally")


if __name__ == "__main__":
    download_data()
