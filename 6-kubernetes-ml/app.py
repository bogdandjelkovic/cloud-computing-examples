from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import pickle
import os

app = Flask(__name__)

PERSISTENT_VOLUME_PATH = "/mnt/data"
DATA_PATH = os.path.join(PERSISTENT_VOLUME_PATH, "wine-quality-white-and-red.csv")
MODEL_PATH = os.path.join(PERSISTENT_VOLUME_PATH, "model.pkl")
FEATURES_PATH = os.path.join(PERSISTENT_VOLUME_PATH, "features.pkl")
TARGET_COLUMN = "quality"

def preprocess_df(df, training=False):
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            if df[col].isnull().any():
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col].fillna(df[col].mean(), inplace=True)

    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        q1 = numeric_df.quantile(0.25)
        q3 = numeric_df.quantile(0.75)
        iqr = q3 - q1
        mask = ~((numeric_df < (q1 - 1.5 * iqr)) | (numeric_df > (q3 + 1.5 * iqr))).any(axis=1)
        df = df[mask]

    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    if not training and os.path.exists(FEATURES_PATH):
        with open(FEATURES_PATH, 'rb') as f:
            feature_columns = pickle.load(f)
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[feature_columns]

    return df

@app.route('/train', methods=['POST'])
def train():
    train_test_perc = request.form.get('train_test_perc')
    try:
        train_test_perc = float(train_test_perc) if train_test_perc else 0.8
    except ValueError:
        return jsonify({'error': '"train_test_perc" must be a valid number'}), 400

    try:
        df = pd.read_csv(DATA_PATH, sep=',')
    except Exception as e:
        return jsonify({'error': f'Could not read CSV: {str(e)}'}), 400

    df = preprocess_df(df, training=True)

    if TARGET_COLUMN not in df.columns:
        return jsonify({'error': f'Target column "{TARGET_COLUMN}" not found'}), 400

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_test_perc, random_state=42, stratify=y)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    os.makedirs(PERSISTENT_VOLUME_PATH, exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(FEATURES_PATH, 'wb') as f:
        pickle.dump(X.columns.tolist(), f)

    return jsonify({
        'Precision': round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 3),
        'Recall': round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 3),
        'F1-Score': round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 3),
        'Accuracy': round(accuracy_score(y_test, y_pred), 3)
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(MODEL_PATH):
        return jsonify({'error': 'Model not trained!'}), 400

    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Field "file" is required'}), 400

    try:
        df = pd.read_csv(file, sep=',')
    except Exception as e:
        return jsonify({'error': f'Invalid CSV file: {str(e)}'}), 400

    df = preprocess_df(df)

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    if TARGET_COLUMN in df.columns:
        X = df.drop(columns=[TARGET_COLUMN])
        y_actual = df[TARGET_COLUMN].tolist()
    else:
        X = df
        y_actual = [None] * len(df)

    preds = model.predict(X).tolist()

    response = []
    for i in range(len(X)):
        response.append({
            "fields": X.iloc[i].to_dict(),
            "actualValue": y_actual[i],
            "predictedValue": preds[i]
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
