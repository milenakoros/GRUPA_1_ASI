
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import joblib
import os
import wandb
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from typing import List

app = FastAPI()

DATABASE_PATH = Path(__file__).parents[2] / "data/08_reporting/api_predictions.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")
engine = create_engine(DATABASE_URL, future=True)

class ModelSingleton:
    _model = None
    _model_version = None
    _model_path = Path(__file__).parents[2] / "data/06_models/ag_production.pkl"
    @classmethod
    def get_model(cls):
        if cls._model is None:
            if cls._model_path.exists():
                print("Loading model from local path...")
                cls._model = joblib.load(cls._model_path)
                cls._model_version = "local"
            else:
                print("Loading model from W&B...")
                run = wandb.init(project="used-car-price-prediction", job_type="api")
                artifact = run.use_artifact("GRUPA_1_ASI/used-car-price-prediction/model_autogluon:production", type="model")
                artifact_dir = artifact.download()
                model_file = os.path.join(artifact_dir, "ag_production.pkl")
                cls._model = joblib.load(model_file)
                cls._model_version = artifact.version
        return cls._model, cls._model_version

def init_db():
    """Initializes the database and creates the predictions table if it doesn't exist."""
    # Ensure the directory for the database exists
    if engine.url.get_backend_name() == "sqlite":
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with engine.begin() as conn:
        if engine.url.get_backend_name() == "sqlite":
            create_table_sql = text("CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY, ts TEXT, payload TEXT, prediction REAL, model_version TEXT)")
        else:
            # For databases like PostgreSQL
            create_table_sql = text("CREATE TABLE IF NOT EXISTS predictions (id SERIAL PRIMARY KEY, ts TIMESTAMP, payload JSONB, prediction DOUBLE PRECISION, model_version TEXT)")
        conn.execute(create_table_sql)
    print(f"Database initialized using engine: {engine.url}")

def save_prediction(payload: dict, prediction: float | int, model_version: str):
    """Saves a prediction to the database."""
    with engine.begin() as conn:
        insert_sql = text("INSERT INTO predictions(ts, payload, prediction, model_version) VALUES (:ts, :payload, :pred, :ver)")
        conn.execute(
            insert_sql,
            {"ts": datetime.now(timezone.utc).isoformat(), "payload": json.dumps(payload), "pred": float(prediction), "ver": model_version},
        )


# This will be called on startup to load the model.
@app.on_event("startup")
async def startup_event():
    init_db()
    ModelSingleton.get_model()

class Features(BaseModel):
    car_name: int
    yr_mfr: int
    fuel_type: int
    kms_run: int
    city: int
    times_viewed: int
    body_type: int
    transmission: int
    variant: int
    assured_buy: int
    registered_city: int
    registered_state: int
    is_hot: int
    rto: int
    source: int
    make: int
    model: int
    car_availability: int
    total_owners: int
    broker_quote: int
    original_price: float
    car_rating: int
    fitness_certificate: int
    emi_starts_from: int
    booking_down_pymnt: int
    reserved: int
    warranty_avail: int

class Prediction(BaseModel):
    prediction: float | int
    model_version: str

class PredictionLog(BaseModel):
    id: int
    ts: str
    payload: dict
    prediction: float
    model_version: str

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(payload: Features):
    model, version = ModelSingleton.get_model()
    input_df = pd.DataFrame([payload.dict()])
    prediction = model.predict(input_df)
    prediction_value = prediction.iloc[0]

    # Log the prediction using the new function
    save_prediction(payload.model_dump(), prediction_value, version)

    return {"prediction": prediction_value, "model_version": version}

@app.get("/predictions", response_model=List[PredictionLog])
def get_predictions():
    """Returns the last 10 predictions from the database."""
    with engine.connect() as conn:
        select_sql = text("SELECT id, ts, payload, prediction, model_version FROM predictions ORDER BY id DESC LIMIT 10")
        results = conn.execute(select_sql).mappings().all()
        # The payload is stored as a string, so we need to parse it back into a dict
        return [{**row, "payload": json.loads(row["payload"])} for row in results]
