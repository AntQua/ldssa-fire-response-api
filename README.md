## Deployed API

The FastAPI application is deployed on Railway and is available at:

- API URL: https://web-production-aa84e.up.railway.app/
- Swagger documentation: https://web-production-aa84e.up.railway.app/docs

## Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check endpoint confirming that the API is running |
| POST | `/predict_response` | Predicts fire department response time in seconds |
| POST | `/actual_response` | Stores the actual response time and returns it together with the previous prediction |

## Example Prediction Request

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
