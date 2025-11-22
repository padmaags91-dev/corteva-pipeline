# corteva-pipeline

This repository contains my end-to-end solution for the Corteva Agriscience Data Engineer coding exercise.

The project shows a full pipeline:

- Ingest raw weather files
- Store them in a relational database
- Compute yearly statistics per weather station
- Expose the data through a REST API with filters, pagination, and Swagger docs

---

## 1. Tech Stack

- **Language:** Python 3
- **Database:** SQLite (via SQLAlchemy ORM)
- **API Framework:** FastAPI + Uvicorn
- **Logging:** Python `logging`
- **Environment:** Local, simple to run

The design can be moved to AWS RDS in production by changing the connection string.

---

## 2. Project Structure

```text
corteva-pipeline/
│
├── wx_data/                 # Raw weather text files (given by Corteva)
│
├── src/
│   ├── models.py            # SQLAlchemy models (stations, observations, yearly stats)
│   ├── db.py                # DB engine, SessionLocal, init_db()
│   ├── ingest_weather.py    # Problem 2: ingestion pipeline
│   └── calc_stats.py        # Problem 3: yearly statistics job
│
├── api/
│   ├── __init__.py
│   └── main.py              # Problem 4: FastAPI app (REST API endpoints)
│
├── weather.db               # SQLite DB file (created after ingestion)
└── README.md
