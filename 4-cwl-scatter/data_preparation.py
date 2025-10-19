import sys
import os
import pandas as pd
from sklearn.model_selection import KFold

def load_data(path):
    return pd.read_csv(path)

def remove_outliers(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    mask = ~((data < (q1 - 1.5 * iqr)) | (data > (q3 + 1.5 * iqr))).any(axis=1)
    return data[mask]

def fill_missing(data):
    return data.fillna(data.mean())

def generate_folds(df, k):
    train_dir = os.path.join("folds", "train")
    test_dir = os.path.join("folds", "test")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    for i, (train_idx, test_idx) in enumerate(kf.split(df)):
        train_df = df.iloc[train_idx]
        test_df = df.iloc[test_idx]

        train_path = os.path.join(train_dir, f"fold_{i}.csv")
        test_path = os.path.join(test_dir, f"fold_{i}.csv")

        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)

def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python data_preparation.py <csv_file> <k_folds>")

    csv_path = sys.argv[1]
    k_folds = int(sys.argv[2])

    df = load_data(csv_path)
    df = remove_outliers(df)
    df = fill_missing(df)

    # Optional: save cleaned dataset
    cleaned_path = "cleaned_dataset.csv"
    df.to_csv(cleaned_path, index=False)

    generate_folds(df, k_folds)

if __name__ == "__main__":
    main()
