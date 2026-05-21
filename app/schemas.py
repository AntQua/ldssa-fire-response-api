from pydantic import BaseModel


# =========================
# predict_response/ request
# =========================

class PredictionRequest(BaseModel):
    call_type: str
    call_type_group: str
    original_priority: str
    unit_id: str
    unit_type: str
    station_area: str
    battalion: str
    neighborhoods_analysis_boundaries: str
    zipcode_of_incident: str
    received_dttm: str


# =========================
# predict_response/ response
# =========================

class PredictionResponse(BaseModel):
    unit_id: str
    received_dttm: str
    predicted_response_time_seconds: float


# =========================
# actual_response/ request
# =========================

class ActualResponseRequest(BaseModel):
    unit_id: str
    received_dttm: str
    on_scene_dttm: str


# =========================
# actual_response/ response
# =========================

class ActualResponseResponse(BaseModel):
    unit_id: str
    received_dttm: str
    on_scene_dttm: str
    actual_response_time_seconds: float
    predicted_response_time_seconds: float