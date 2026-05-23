from pathlib import Path

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "xgb_response_time_pipeline.pkl"

model = joblib.load(MODEL_PATH)


DEFAULT_FEATURE_VALUES = {
    "call_type": "Unknown",
    "call_type_group": "Unknown",
    "original_priority": "Unknown",
    "unit_type": "Unknown",
    "station_area": "Unknown",
    "battalion": "Unknown",
    "neighborhoods_analysis_boundaries": "Unknown",
    "neighborhood_district": "Unknown",
    "zipcode_of_incident": "Unknown",
}


def add_default_feature_values(request_data: dict) -> dict:
    prepared_data = request_data.copy()

    for column, default_value in DEFAULT_FEATURE_VALUES.items():
        value = prepared_data.get(column)

        if value is None or value == "":
            prepared_data[column] = default_value

    return prepared_data


def predict_response_time(request_data: dict) -> float:
    prepared_data = add_default_feature_values(request_data)

    input_df = pd.DataFrame([prepared_data])

    received_dt = pd.to_datetime(input_df["received_dttm"])

    input_df["hour"] = received_dt.dt.hour
    input_df["month"] = received_dt.dt.month
    input_df["day_of_week"] = received_dt.dt.dayofweek

    input_df["is_weekend"] = input_df["day_of_week"].isin([5, 6]).astype(int)
    input_df["is_night"] = input_df["hour"].between(0, 5).astype(int)

    input_df["is_rush_hour"] = input_df["hour"].isin(
        [7, 8, 9, 16, 17, 18]
    ).astype(int)

    input_df["hour_sin"] = np.sin(2 * np.pi * input_df["hour"] / 24)
    input_df["hour_cos"] = np.cos(2 * np.pi * input_df["hour"] / 24)

    input_df["dow_sin"] = np.sin(2 * np.pi * input_df["day_of_week"] / 7)
    input_df["dow_cos"] = np.cos(2 * np.pi * input_df["day_of_week"] / 7)

    prediction = model.predict(input_df)[0]

    return float(prediction)