"""
This is a boilerplate test file for pipeline 'data_science'
generated using Kedro 1.0.0.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""

import pandas as pd
import numpy as np
import pytest
from sklearn.ensemble import RandomForestRegressor
from kedro.pipeline import Pipeline

from unittest.mock import patch, MagicMock
from used_car_price_prediction.pipelines.data_science.nodes import (
    basic_clean,
    split_to_train_test,
    train_baseline,
    evaluate,
)
from used_car_price_prediction.pipelines.data_science.pipeline import create_pipeline

@pytest.fixture
def dummy_raw_df():
    data = {
        'original_price': [100000, np.nan],
        'sale_price': [90000, 80000],
        'car_availability': ['In Stock', np.nan],
        'transmission': ['Manual', np.nan],
        'source': ['SourceA', None],
        'body_type': ['Sedan', 'SUV'],
        'registered_city': ['CityA', 'CityB'],
        'registered_state': ['StateA', 'StateB'],
        'car_rating': [4.5, None],
        'fitness_certificate': [True, False],
        'ad_created_on': ['2023-01-01', '2023-01-02'],
        'kms_run': [50000, 200000],
        'times_viewed': [100, 9000],
        'total_owners': [1, 5],
        'assured_buy': [True, False],
        'is_hot': [False, True],
        'reserved': [True, False],
        'warranty_avail': [False, True],
        'fuel_type': ['Petrol', 'Diesel'],
        'city': ['CityA', 'CityB'],
        'variant': ['V1', 'V2'],
        'rto': ['RTO1', 'RTO2'],
        'make': ['Make1', 'Make2'],
        'model': ['Model1', 'Model2'],
        'yr_mfr': [2018, 2019],
        'car_name': ['Car1', 'Car2'],
        'broker_quote': [95000, 85000],
        'emi_starts_from': [2000, 1800],
        'booking_down_pymnt': [10000, 8000]
    }
    return pd.DataFrame(data)


class TestDataScienceNodes:

    def test_data_science_pipeline_creation(self):
        pipeline = create_pipeline()

        assert isinstance(pipeline, Pipeline)
        assert len(pipeline.nodes) == 5
        # You could even check specific node connections
        assert "clean_data" in pipeline.all_outputs()
        assert "X_train" in pipeline.all_outputs()

    def test_basic_clean(self, dummy_raw_df):
        cleaned_df = basic_clean(dummy_raw_df)

        # After dropping NaNs, only 1 row should remain
        assert len(cleaned_df) == 1
        # Check if values were clipped
        assert cleaned_df['kms_run'].iloc[0] == 50000
        assert cleaned_df['times_viewed'].iloc[0] == 100
        assert cleaned_df['total_owners'].iloc[0] == 1
        # Check if 'ad_created_on' is dropped
        assert 'ad_created_on' not in cleaned_df.columns
        # Check if original_price was filled
        assert cleaned_df['original_price'].notna().all()

    def test_split_to_train_test(self):
        df = pd.DataFrame({
            'feature1': range(100),
            'feature2': range(100, 200),
            'sale_price': range(200, 300)
        })
        test_size = 0.2
        X_train, X_test, y_train, y_test = split_to_train_test(df, test_size, 42)

        assert len(X_train) == 80
        assert len(y_train) == 80
        assert len(X_test) == 20
        assert len(y_test) == 20
        assert 'sale_price' not in X_train.columns
        assert 'sale_price' not in X_test.columns

    def test_train_baseline(self):
        X_train = pd.DataFrame({'feature1': [1, 2, 3]})
        y_train = pd.Series([1, 2, 3])
        params = {'random_state': 42, 'n_estimators': 10, 'criterion': 'squared_error'}

        model = train_baseline(X_train, y_train, params)
        assert isinstance(model, RandomForestRegressor)

    @patch("used_car_price_prediction.pipelines.data_science.nodes.wandb") # Ta linijka jest mocarna
    def test_evaluate(self, mock_wandb):
        mock_artifact = MagicMock()
        mock_wandb.Artifact.return_value = mock_artifact

        model = RandomForestRegressor().fit(pd.DataFrame({'f': [1,2]}), pd.Series([1,2]))
        X_test = pd.DataFrame({'f': [1, 2, 3]})
        y_test = pd.Series([1, 2, 3.5])

        # Mock wandb to avoid actual logging during tests
        metrics = evaluate(model, X_test, y_test)

        assert "RMSE" in metrics
        assert isinstance(metrics["RMSE"], float)

        mock_wandb.init.assert_called_once()
        mock_wandb.log.assert_called_once_with(metrics)
        mock_wandb.Artifact.assert_called_once_with("model_baseline", type="model")
        mock_wandb.log_artifact.assert_called_once_with(mock_artifact)
        mock_wandb.finish.assert_called_once()
