# Fire Department Response Time API

This project was developed as part of the LDSSA (Lisbon Data Science Starters Academy) Capstone Project.

The objective of the project is to deploy a machine learning model capable of predicting Fire Department response times based on incident information from the San Francisco Fire Department Calls for Service dataset.

The application was built using FastAPI and deployed on Railway.

---

# Project Overview

The API allows users to:

- Predict estimated fire department response times
- Store predictions in a SQLite database
- Submit actual response times after the incident occurs
- Compare predicted vs actual response times
- Validate incoming requests before running the machine learning model

The deployed model uses an XGBoost pipeline trained on historical emergency call data.

---

# Tech Stack

- Python
- FastAPI
- XGBoost
- Scikit-learn
- Pandas
- SQLite
- Railway
- Uvicorn

---

# Deployed API

The FastAPI application is deployed on Railway and is available at:

- API URL: https://web-production-aa84e.up.railway.app/
- Swagger documentation: https://web-production-aa84e.up.railway.app/docs

---

# Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check endpoint confirming that the API is running |
| POST | `/predict_response` | Predicts fire department response time in seconds |
| POST | `/actual_response` | Stores the actual response time and returns it together with the previous prediction |

---

# Example Prediction Request

## Endpoint

```txt
POST /predict_response
````

## Request Body

```json
{
  "call_type": "Medical Incident",
  "call_type_group": "Potential Life Threatening",
  "original_priority": "3",
  "unit_id": "52",
  "unit_type": "ENGINE",
  "station_area": "1",
  "battalion": "B01",
  "neighborhoods_analysis_boundaries": "Financial District/South Beach",
  "neighborhood_district": "Financial District/South Beach",
  "zipcode_of_incident": "94105",
  "received_dttm": "2025-01-01T02:10:43"
}
```

## Example Response

```json
{
  "unit_id": "52",
  "received_dttm": "2025-01-01T02:10:43",
  "predicted_response_time_seconds": 463.18
}
```

---

# Example Actual Response Request

## Endpoint

```txt
POST /actual_response
```

## Request Body

```json
{
  "unit_id": "52",
  "received_dttm": "2025-01-01T02:10:43",
  "on_scene_dttm": "2025-01-01T02:20:43"
}
```

## Example Response

```json
{
  "unit_id": "52",
  "received_dttm": "2025-01-01T02:10:43",
  "on_scene_dttm": "2025-01-01T02:20:43",
  "actual_response_time_seconds": 600.0,
  "predicted_response_time_seconds": 463.18
}
```

---

# Validation Behavior

The API performs input validation before calling the machine learning model.

Known validation behavior:

* Missing required fields return HTTP `422`
* Invalid datetime values return HTTP `422`
* Unknown categorical values return HTTP `422`
* `/actual_response` returns HTTP `422` if no previous prediction exists
* `/actual_response` returns HTTP `422` if `on_scene_dttm` is earlier than `received_dttm`

## Example Invalid Category Response

```json
{
  "detail": "Unrecognised value for call_type: Alien Invasion"
}
```

---

# Local Development

## Create virtual environment

```bash
python -m venv .venv
```

## Activate virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / MacOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run locally

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

---

# Deployment

The application is deployed using Railway.

Deployment includes:

* FastAPI application
* Uvicorn server
* SQLite database
* Trained XGBoost pipeline
* Automatic redeployment from GitHub

---

# Repository Structure

```txt
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── model_utils.py
│   ├── schemas.py
│
├── models/
│   ├── xgb_response_time_pipeline.pkl
│   ├── feature_metadata.pkl
│
├── requirements.txt
├── Procfile
├── README.md
```

---

# Author

António Quaresma

LDSSA - Lisbon Data Science Starters Academy
Capstone Project


```

