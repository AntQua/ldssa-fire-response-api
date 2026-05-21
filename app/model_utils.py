import joblib
import pandas as pd
from pathlib import Path


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
    prediction = model.predict(input_df)[0]
    return float(prediction)