
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import wandb
import pandas as pd
from pathlib import Path

from pydantic import BaseModel 

app = FastAPI() 

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
                # The user requested "TEAM/ag_model:production", but based on your project structure,
                # the correct artifact path seems to be "GRUPA_1_ASI/used-car-price-prediction/model_autogluon:production"
                # Please verify the team/entity and project name in your W&B account.
                artifact = run.use_artifact("GRUPA_1_ASI/used-car-price-prediction/model_autogluon:production", type="model")
                artifact_dir = artifact.download()
                model_file = os.path.join(artifact_dir, "ag_production.pkl")
                cls._model = joblib.load(model_file)
                cls._model_version = artifact.version
        return cls._model, cls._model_version

# This will be called on startup to load the model.
@app.on_event("startup")
async def startup_event():
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


@app.get("/healthz") 
def healthz(): 
    return {"status": "ok"} 


@app.post("/predict", response_model=Prediction) 
def predict(payload: Features): 
    model, version = ModelSingleton.get_model()
    # Create a DataFrame from the payload for prediction
    # The column names must match what the model was trained on.
    # This is just an example.
    input_df = pd.DataFrame([payload.dict()])
    prediction = model.predict(input_df)
    return {"prediction": prediction.iloc[0], "model_version": version}
