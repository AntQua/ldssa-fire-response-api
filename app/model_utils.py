import os
import joblib
import numpy as np
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "xgb_response_time_pipeline.pkl",
)


model_pipeline = joblib.load(MODEL_PATH)


def build_features(request_data: dict) -> pd.DataFrame:
    """
    Convert one API request into the same feature format used during training.
    """

    received_dttm = pd.to_datetime(request_data["received_dttm"], errors="coerce")

    if pd.isna(received_dttm):
        raise ValueError("Invalid received_dttm format.")

    hour = received_dttm.hour
    day_of_week = received_dttm.dayofweek
    month = received_dttm.month

    features = {
        "call_type": request_data["call_type"],
        "call_type_group": request_data.get("call_type_group", "UNKNOWN"),
        "original_priority": request_data.get("original_priority", "UNKNOWN"),
        "unit_id": request_data["unit_id"],
        "unit_type": request_data["unit_type"],
        "station_area": str(request_data["station_area"]),
        "battalion": request_data["battalion"],
        "neighborhoods_analysis_boundaries": request_data.get(
            "neighborhoods_analysis_boundaries",
            "UNKNOWN",
        ),
        "zipcode_of_incident": str(request_data["zipcode_of_incident"]),
        "hour": hour,
        "day_of_week": day_of_week,
        "month": month,
        "is_weekend": int(day_of_week >= 5),
        "is_rush_hour": int(
            (7 <= hour <= 9) or (16 <= hour <= 18)
        ),
        "is_night": int(
            (hour >= 22) or (hour <= 5)
        ),
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
        "dow_sin": np.sin(2 * np.pi * day_of_week / 7),
        "dow_cos": np.cos(2 * np.pi * day_of_week / 7),
    }

    return pd.DataFrame([features])


def predict_response_time(request_data: dict) -> float:
    """
    Predict response time in seconds.
    """

    features_df = build_features(request_data)

    prediction = model_pipeline.predict(features_df)[0]

    return float(max(prediction, 0))