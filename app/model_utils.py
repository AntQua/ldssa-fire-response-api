import joblib
import pandas as pd
from pathlib import Path
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "xgb_response_time_pipeline.pkl"

model = joblib.load(MODEL_PATH)


KNOWN_CATEGORIES = {
    "call_type": {
        "Medical Incident",
        "Structure Fire",
        "Alarms",
        "Traffic Collision",
        "Citizen Assist / Service Call",
        "Other",
        "Outside Fire",
        "Vehicle Fire",
        "Water Rescue",
        "Gas Leak (Natural and LP Gases)",
        "Electrical Hazard",
        "Elevator / Escalator Rescue",
        "Fuel Spill",
        "Smoke Investigation (Outside)",
        "Odor (Strange / Unknown)",
        "Assist Police",
        "Explosion",
        "HazMat",
        "Industrial Accidents",
        "Mutual Aid / Assist Outside Agency",
        "Train / Rail Incident",
        "Train / Rail Fire",
        "Aircraft Emergency",
        "Marine Fire",
        "Watercraft in Distress",
        "Confined Space / Structure Collapse",
        "Extrication / Entrapped (Machinery, Vehicle)",
        "High Angle Rescue",
        "Lightning Strike (Investigation)",
        "Oil Spill",
        "Suspicious Package",
        "Administrative",
        "Transfer",
    },
    "call_type_group": {
        "Fire",
        "Alarm",
        "Potential Life Threatening",
        "Non Life Threatening",
    },
    "original_priority": {
        "2",
        "3",
    },
    "unit_type": {
        "ENGINE",
        "TRUCK",
        "MEDIC",
        "CHIEF",
        "PRIVATE",
        "RESCUE SQUAD",
        "RESCUE CAPTAIN",
        "SUPPORT",
        "AIRPORT",
        "INVESTIGATION",
    },
}


def validate_known_categories(request_data: dict) -> None:
    for field, valid_values in KNOWN_CATEGORIES.items():
        value = request_data.get(field)

        if value is None:
            raise ValueError(f"Missing required field: {field}")

        value = str(value)

        if value not in valid_values:
            raise ValueError(
                f"Unrecognised value for {field}: {value}"
            )


def predict_response_time(request_data: dict) -> float:
    input_df = pd.DataFrame([request_data])

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