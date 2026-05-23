from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    call_type: str
    call_type_group: str
    original_priority: str
    unit_id: str
    unit_type: str
    station_area: str
    battalion: str
    neighborhoods_analysis_boundaries: str
    neighborhood_district: Optional[str] = None
    zipcode_of_incident: str
    received_dttm: str


class PredictionResponse(BaseModel):
    unit_id: str
    received_dttm: str
    predicted_response_time_seconds: float


class ActualResponseRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    unit_id: str
    received_dttm: str
    on_scene_dttm: str


class ActualResponseResponse(BaseModel):
    unit_id: str
    received_dttm: str
    on_scene_dttm: str
    actual_response_time_seconds: float
    predicted_response_time_seconds: float