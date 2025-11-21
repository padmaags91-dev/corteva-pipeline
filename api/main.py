from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from src.db import SessionLocal, init_db
from src.models import WeatherObservation, WeatherStatsYearly, WeatherStation

app = FastAPI(
    title="Corteva Weather API",
    description="REST API for weather data and yearly statistics",
    version="1.0.0",
)


# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/weather")
def get_weather(
    station_id: Optional[int] = None,
    date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(WeatherObservation)

    if station_id:
        query = query.filter(WeatherObservation.station_id == station_id)

    if date:
        query = query.filter(WeatherObservation.obs_date == date)

    total = query.count()

    items = (
        query.order_by(WeatherObservation.obs_date)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": [
            {
                "station_id": x.station_id,
                "date": x.obs_date.isoformat(),
                "max_temp": x.max_temp_tenth_c,
                "min_temp": x.min_temp_tenth_c,
                "precip_mm": x.precip_tenth_mm,
            }
            for x in items
        ],
    }


@app.get("/api/weather/stats")
def get_weather_stats(
    station_id: Optional[int] = None,
    year: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(WeatherStatsYearly)

    if station_id:
        query = query.filter(WeatherStatsYearly.station_id == station_id)

    if year:
        query = query.filter(WeatherStatsYearly.year == year)

    total = query.count()

    items = (
        query.order_by(WeatherStatsYearly.year)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": [
            {
                "station_id": x.station_id,
                "year": x.year,
                "avg_max_temp_c": x.avg_max_temp_c,
                "avg_min_temp_c": x.avg_min_temp_c,
                "total_precip_cm": x.total_precip_cm,
            }
            for x in items
        ],
    }

