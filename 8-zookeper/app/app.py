import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from kazoo.client import KazooClient
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

app = FastAPI(title="8-zookeper")

MODEL_ZNODE = '/ml_model'

zk = KazooClient(hosts="localhost:2181")

connected = False
for _ in range(10):
    try:
        zk.start(timeout=5)
        connected = True
        break
    except:
        print("ZooKeeper not ready, retrying...")
        time.sleep(3)

if not connected:
    raise Exception("Could not connect to ZooKeeper!")

model = LinearRegression()
MODEL_FILE = 'local_model.pkl'

if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

def sync_model_to_zk(model):
    data = pickle.dumps(model)
    if zk.exists(MODEL_ZNODE):
        zk.set(MODEL_ZNODE, data)
    else:
        zk.create(MODEL_ZNODE, data)

def load_model_from_zk():
    if zk.exists(MODEL_ZNODE):
        data, _ = zk.get(MODEL_ZNODE)
        return pickle.loads(data)
    return None

class PredictRequest(BaseModel):
    features: list[float]

@app.put("/model", summary="Update ML model using CSV file")
async def update_model(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV file required")

    df = pd.read_csv(file.file)
    if 'target' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must have a target column 'target'")

    X = df.drop(columns=['target'])
    y = df['target']

    global model
    model = LinearRegression()
    model.fit(X, y)

    
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)

    
    sync_model_to_zk(model)

    return {"message": "Model updated successfully"}

@app.post("/predict", summary="Get prediction using current ML model")
async def predict(req: PredictRequest):
    features = req.features

    latest_model = load_model_from_zk()
    if latest_model:
        global model
        model = latest_model

    pred = model.predict([features])
    return {"prediction": float(pred[0])}

sync_model_to_zk(model)
