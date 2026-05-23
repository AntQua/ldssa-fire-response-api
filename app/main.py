from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import (
    PredictionRequest,
    PredictionResponse,
    ActualResponseRequest,
    ActualResponseResponse,
)

from app.model_utils import predict_response_time

from app.database import (
    initialize_database,
    insert_prediction,
    get_prediction,
    update_actual_response,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Fire Department Response Time API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Fire Department Response Time API is running."
    }


@app.post(
    "/predict_response",
    response_model=PredictionResponse,
)
@app.post(
    "/predict_response/",
    response_model=PredictionResponse,
    include_in_schema=False,
)
def predict_response(request: PredictionRequest):

    try:
        request_data = request.model_dump()

        predicted_response_time = predict_response_time(request_data)

        insert_prediction(
            unit_id=request.unit_id,
            received_dttm=request.received_dttm,
            predicted_response_time_seconds=predicted_response_time,
        )

        return PredictionResponse(
            unit_id=request.unit_id,
            received_dttm=request.received_dttm,
            predicted_response_time_seconds=round(
                predicted_response_time,
                2,
            ),
        )

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )


@app.post(
    "/actual_response",
    response_model=ActualResponseResponse,
)
@app.post(
    "/actual_response/",
    response_model=ActualResponseResponse,
    include_in_schema=False,
)
def actual_response(request: ActualResponseRequest):

    try:
        stored_prediction = get_prediction(
            unit_id=request.unit_id,
            received_dttm=request.received_dttm,
        )

        if stored_prediction is None:
            raise HTTPException(
                status_code=422,
                detail="Prediction record not found.",
            )

        (
            unit_id,
            received_dttm,
            predicted_response_time_seconds,
        ) = stored_prediction

        received_dt = pd.to_datetime(received_dttm)
        on_scene_dt = pd.to_datetime(request.on_scene_dttm)

        actual_response_time_seconds = (
            on_scene_dt - received_dt
        ).total_seconds()

        if actual_response_time_seconds < 0:
            raise HTTPException(
                status_code=422,
                detail="Negative response time detected.",
            )

        update_actual_response(
            unit_id=request.unit_id,
            received_dttm=request.received_dttm,
            on_scene_dttm=request.on_scene_dttm,
            actual_response_time_seconds=actual_response_time_seconds,
        )

        return ActualResponseResponse(
            unit_id=request.unit_id,
            received_dttm=request.received_dttm,
            on_scene_dttm=request.on_scene_dttm,
            actual_response_time_seconds=round(
                actual_response_time_seconds,
                2,
            ),
            predicted_response_time_seconds=round(
                predicted_response_time_seconds,
                2,
            ),
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )