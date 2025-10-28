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

    return df
