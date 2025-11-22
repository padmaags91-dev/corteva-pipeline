# corteva-pipeline

Corteva Weather Data Engineering Pipeline

By: Sri Padmavathi Manoharan, Data Engineer 

This project is an end-to-end data engineering solution that processes 30 years of U.S. weather station data and exposes it through a fully documented REST API. It demonstrates real production-grade patterns: ingestion, validation, modeling, aggregation, API design, and idempotent processing.

Project Overview

This pipeline covers:

Raw Data Ingestion (1.7M+ weather records)

Database Modeling (normalized schema with SQLAlchemy)

Data Cleaning & Missing Data Handling

Idempotent Load Process

Yearly Statistics Calculation (avg temps, total precipitation)

REST API (FastAPI)

Filtering + Pagination

Swagger UI + OpenAPI Schema

Production-ready project structure

Project Structure
corteva-pipeline/
│
├── api/                     # FastAPI backend
│   └── main.py
│
├── src/                     # Core pipeline logic
│   ├── db.py                # DB connection + initialization
│   ├── models.py            # ORM models
│   ├── ingest_weather.py    # Raw data ingestion
│   └── calc_stats.py        # Yearly metric aggregation
│
├── wx_data/                 # Raw data files (1985–2014)
├── weather.db               # SQLite database
├── screenshots/             # Added screenshots for HR review
└── README.md

1. Data Ingestion

Command:

python -m src.ingest_weather


What happens:

Reads 167 weather station files

Cleans missing values (-9999)

Normalizes raw temperature/precipitation

Loads into SQLite

Prevents duplicates (idempotent)

Example Output (Screenshot):

Finished weather ingestion | files=167, inserted=0, skipped=1729957


See screenshots/screenshot_ingestion_log.png

2. Yearly Statistics Calculation

Command:

python -m src.calc_stats


This creates aggregated metrics for each station:

Average max temperature (°C)

Average min temperature (°C)

Total precipitation (cm)

Screenshot:
 screenshots/screenshot_stats_job.png

3. Start the REST API

Command:

uvicorn api.main:app --reload


Your API will run at:

http://127.0.0.1:8000


Screenshot:
screenshots/screenshot_api_running.png

4. API Documentation (Swagger UI)

Open in browser:

http://127.0.0.1:8000/docs


Automatically generated via OpenAPI

Each endpoint testable from UI

Supports pagination + filters

Screenshot:
screenshots/screenshot_swagger_ui.png

5. API Endpoints
GET /api/weather

Returns daily weather records.

Example:

http://127.0.0.1:8000/api/weather?page=1&page_size=5


Sample Output:

{
  "total": 1729957,
  "page": 1,
  "page_size": 5,
  "results": [
    {
      "station_id": 1,
      "date": "1985-01-01",
      "max_temp": -83,
      "min_temp": -144,
      "precip_mm": 0
    },
    ...
  ]
}


Screenshot:
screenshots/screenshot_weather_api_response.png

GET /api/weather/stats

Returns yearly aggregated metrics per station.

Example:

http://127.0.0.1:8000/api/weather/stats?page=1&page_size=5

Technologies Used

Python 3.11

SQLAlchemy ORM

SQLite (lightweight DB for demo)

FastAPI

Uvicorn

Logging

Pagination & Query Filters

Data Normalization

OpenAPI + Swagger
