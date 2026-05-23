from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    unit_id: str
    received_dttm: str

    call_type: Optional[str] = "Unknown"
    call_type_group: Optional[str] = "Unknown"
    original_priority: Optional[str] = "Unknown"
    unit_type: Optional[str] = "Unknown"
    station_area: Optional[str] = "Unknown"
    battalion: Optional[str] = "Unknown"
    neighborhoods_analysis_boundaries: Optional[str] = "Unknown"
    neighborhood_district: Optional[str] = "Unknown"
    zipcode_of_incident: Optional[str] = "Unknown"


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