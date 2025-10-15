import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

def load_data(path):
    return pd.read_csv(path)

def split_features_target(df, target):
    X = df.drop(columns=[target])
    y = df[target]

    return X, y

def train_model(X_train, y_train):
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    return reg

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)

    return rmse

def main(args):
    dataset_path, target_col, train_pct = args[1], args[2], float(args[3])
    df = load_data(dataset_path)
    X, y = split_features_target(df, target_col)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_pct)
    model = train_model(X_train, y_train)
    rmse = evaluate_model(model, X_test, y_test)
    print(f"Calculated RMSE: {rmse:.4f}")

if __name__ == "__main__":
    main(sys.argv)