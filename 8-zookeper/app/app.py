import time
import os
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from kazoo.client import KazooClient
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score, f1_score, accuracy_score

app = FastAPI(title="8-zookeeper-ML")

MODEL_ZNODE = '/ml_pipeline'
INFO_ZNODE = '/ml_pipeline_info'

zk = KazooClient(hosts=os.getenv("ZOO_HOSTS", "127.0.0.1:2181"))

connected = False
for _ in range(10):
    try:
        zk.start(timeout=5)
        connected = True
        break
    except Exception:
        print("zookeeper not ready, retrying...")
        time.sleep(3)

if not connected:
    raise Exception("failed to connect to zookeeper!")

MODEL_FILE = 'local_pipeline.pkl'
INFO_FILE = 'local_pipeline_info.pkl'

pipeline = None
model_info = None


def sync_to_zk(znode: str, data_obj):
    print(f"{znode} syncing...")
    data = pickle.dumps(data_obj)
    if zk.exists(znode):
        zk.set(znode, data)
        print(f"{znode} updated")
    else:
        zk.create(znode, data)
        print(f"{znode} created")


def load_from_zk(znode: str):
    if zk.exists(znode):
        data, _ = zk.get(znode)
        return pickle.loads(data)
    return None


def save_local(file_path: str, obj):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)


def load_local(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None


pipeline = load_local(MODEL_FILE) or load_from_zk(MODEL_ZNODE)
model_info = load_local(INFO_FILE) or load_from_zk(INFO_ZNODE)


class PredictRequest(BaseModel):
    features: dict[str, object]


@app.put("/model")
async def update_model(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    train_test_split_ratio: float = Form(0.8)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400)

    df = pd.read_csv(file.file)

    if target_column not in df.columns:
        raise HTTPException(status_code=400)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    cat_cols = X.select_dtypes(include=['object', 'category']).columns
    num_cols = X.select_dtypes(exclude=['object', 'category']).columns

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="mean"))
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols)
        ]
    )

    if pd.api.types.is_numeric_dtype(y):
        model_type = LinearRegression()
        problem_type = "regression"
    else:
        model_type = LogisticRegression(max_iter=500)
        problem_type = "classification"

    pipeline_new = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model_type)
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_test_split_ratio)

    pipeline_new.fit(X_train, y_train)

    y_pred = pipeline_new.predict(X_test)
    if problem_type == "regression":
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        stats = {"RMSE": rmse, "R2": r2}
    else:
        y_test_enc = pd.factorize(y_test)[0]
        y_pred_enc = pd.factorize(y_pred)[0]
        f1 = f1_score(y_test_enc, y_pred_enc, average="weighted")
        acc = accuracy_score(y_test_enc, y_pred_enc)
        stats = {"Accuracy": acc, "F1": f1}

    model_info_new = {
        "name": file.filename,
        "target_col": target_column,
        "model": "LinearRegression" if problem_type == "regression" else "LogisticRegression",
        "problem_type": problem_type,
        "stats": stats
    }

    save_local(MODEL_FILE, pipeline_new)
    save_local(INFO_FILE, model_info_new)
    sync_to_zk(MODEL_ZNODE, pipeline_new)
    sync_to_zk(INFO_ZNODE, model_info_new)

    global pipeline, model_info
    pipeline = pipeline_new
    model_info = model_info_new

    return {
        "message": f"{problem_type.title()} model trained and synced to ZooKeeper",
        "info": model_info_new
    }


@app.post("/predict")
async def predict(req: PredictRequest):
    latest_pipeline = load_from_zk(MODEL_ZNODE)
    if latest_pipeline:
        global pipeline
        pipeline = latest_pipeline

    if not pipeline:
        raise HTTPException(status_code=500)

    X_new = pd.DataFrame([req.features])

    try:
        pred = pipeline.predict(X_new)
        result = pred[0]
        if hasattr(pipeline.named_steps["model"], "classes_"):
            result = str(result)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=400)


@app.get("/model")
async def get_model_info():
    global model_info
    if not model_info:
        model_info = load_from_zk(INFO_ZNODE)
        if not model_info:
            model_info = load_local(INFO_FILE)

    if not model_info:
        raise HTTPException(status_code=404)

    return model_info

def zk_model_watch(data, stat, event):
    global pipeline, model_info
    print(f"znode changed, reloading...")
    if data:
        pipeline = pickle.loads(data) if event.path == MODEL_ZNODE else pipeline
        model_info = pickle.loads(data) if event.path == INFO_ZNODE else model_info

zk.DataWatch(MODEL_ZNODE, zk_model_watch)
zk.DataWatch(INFO_ZNODE, zk_model_watch)

if pipeline:
    sync_to_zk(MODEL_ZNODE, pipeline)

if model_info:
    sync_to_zk(INFO_ZNODE, model_info)
