"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.0.0
"""

import pandas as pd
import numpy as np
import seaborn as sns
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from kedro_datasets.json import JSONDataset
from kedro_datasets.pickle import PickleDataset
from autogluon.tabular import TabularPredictor
import wandb

from .df_structure import columns

def load_raw(df: pd.DataFrame) -> pd.DataFrame:
    return df

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Usuwanie Braków
    df['original_price'].fillna(df['sale_price'], inplace = True)
    df['car_availability'].fillna('NaN', inplace = True)
    df['transmission'].fillna('NaN', inplace = True)
    df = df.dropna(subset=[
        'source',
        'body_type',
        'registered_city',
        'registered_state',
        'car_rating',
        'fitness_certificate',
        'ad_created_on'
    ])

    # Przycinanie wartości
    df['kms_run'] = df['kms_run'].clip(upper=150000)
    df['times_viewed'] = df['times_viewed'].clip(upper=8000)
    df['total_owners'] = df['total_owners'].clip(upper=3)

    # Zakodowanie cech kategorycznych
    for column_label in columns['CATEGORICAL']:
        df[column_label] = df[column_label].astype(str)
        df[column_label].fillna('NAN', inplace=True)
        df[column_label] = df[column_label].astype('category').cat.codes.astype(int)

    # Zakodowanie cech logicznych
    for column_label in columns['BOOLEAN']:
        df[column_label] = df[column_label].astype(int)

    # (TYMACZASOWE) Usunięcie szkodliwej kolumny
    df = df.drop(columns='ad_created_on')

    return df

def split_to_train_test(df: pd.DataFrame, test_size: float, random_state: int) -> pd.DataFrame:
    x = df.drop('sale_price', axis=1)
    y = df['sale_price']
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test

def train_baseline(X_train: pd.DataFrame, y_train: pd.DataFrame, params: dict) -> PickleDataset:
    model = RandomForestRegressor(
        random_state=params['random_state'],
        n_estimators=params['n_estimators'],
        criterion=params['criterion']
    )

    model.fit(X_train, y_train)

    return model

def evaluate(model: PickleDataset, X_test: pd.DataFrame, y_test: pd.DataFrame) -> JSONDataset:
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    metrics = {"RMSE": float(round(rmse, 2))}

    # Log do W&B
    wandb.init(project="used-car-price-prediction", job_type="evaluate", reinit=True)
    wandb.log(metrics)

    art = wandb.Artifact("model_baseline", type="model")
    art.add_file("data/06_models/model_baseline.pkl")
    wandb.log_artifact(art)

    wandb.finish()

    return metrics

def train_autogluon(X_train: pd.DataFrame, y_train: pd.DataFrame, params: dict, random_state: int) -> TabularPredictor:
    train_data = X_train.copy()
    train_data[params["label"]] = y_train

    predictor = TabularPredictor(
        label=params["label"],
        problem_type=params.get("problem_type"),
        eval_metric=params.get("eval_metric"),
        path="autogluon"
    ).fit(
        train_data=train_data,
        time_limit=params.get("time_limit"),
        presets=params.get("presets"),
        ag_args_fit={'random_state': random_state}
    )

    return predictor

def evaluate_autogluon(ag_predictor: TabularPredictor, X_test: pd.DataFrame, y_test: pd.DataFrame, params: dict) -> dict:
    y_test_series = y_test.squeeze()

    predictions = ag_predictor.predict(X_test)
    perf = ag_predictor.evaluate_predictions(y_true=y_test_series, y_pred=predictions)

    # Log metrics to W&B
    notes = f"AutoGluon params: {params}"
    wandb.init(project="used-car-price-prediction", job_type="evaluate_autogluon", reinit=True, config=ag_predictor.fit_summary(), notes=notes)
    wandb.log(perf)

    art = wandb.Artifact("model_autogluon", type="model")
    art.add_file("data/06_models/ag_production.pkl")
    wandb.log_artifact(art, aliases=["production"])    # aliases=["production"] dla najlepszego modelu; aliases=["candidate"]  dla modelu kandydującego

    X_test_with_label = X_test.copy()
    X_test_with_label["sale_price"] = y_test

    # Feature importance
    importance = ag_predictor.feature_importance(data=X_test_with_label, model=None)
    plt.figure(figsize=(8, 6))
    importance["importance"].plot(kind="barh")
    plt.title("Feature Importance (AutoGluon)")
    plt.tight_layout()
    wandb.log({"feature_importance": wandb.Image(plt)})
    wandb.finish()

    return perf
