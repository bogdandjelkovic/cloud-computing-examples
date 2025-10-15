import sys
import pandas as pd

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

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python model_training.py <csv_file>")

    df = load_data(sys.argv[1])
    df = remove_outliers(df)
    df = fill_missing(df)

    sys.stdout.write(df.to_csv(index=False))

if __name__ == "__main__":
    main()
