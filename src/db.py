from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

# Local SQLite DB for this exercise.
# In production, this would be PostgreSQL on RDS or similar.
DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required by SQLite sometimes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Create all tables if they don't exist.
    Safe to call multiple times.
    """
    Base.metadata.create_all(bind=engine)
