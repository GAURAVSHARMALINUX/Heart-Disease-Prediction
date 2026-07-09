import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

def download_data(output_dir="data"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("Fetching Heart Disease dataset from UCI...")
    heart_disease = fetch_ucirepo(id=45) 
    
    # data (as pandas dataframes) 
    X = heart_disease.data.features 
    y = heart_disease.data.targets 
    
    df = pd.concat([X, y], axis=1)
    
    output_path = os.path.join(output_dir, "heart.csv")
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    download_data()
