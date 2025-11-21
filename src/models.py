from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WeatherStation(Base):
    """
    One row per weather station (per file).
    """
    __tablename__ = "weather_station"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_code = Column(String, nullable=False, unique=True)  # from filename
    state_code = Column(String, nullable=True)                   # e.g. NE, IA, IL, IN, OH
    name = Column(String, nullable=True)                         # optional description

    observations = relationship("WeatherObservation", back_populates="station")
    stats = relationship("WeatherStatsYearly", back_populates="station")


class WeatherObservation(Base):
    """
    Raw daily weather data:
    one row per station per date.
    """
    __tablename__ = "weather_observation"

    station_id = Column(Integer, ForeignKey("weather_station.id"), primary_key=True)
    obs_date = Column(Date, primary_key=True)

    # -9999 from the raw file will be stored as NULL (None)
    max_temp_tenth_c = Column(Integer, nullable=True)   # tenths of °C
    min_temp_tenth_c = Column(Integer, nullable=True)   # tenths of °C
    precip_tenth_mm = Column(Integer, nullable=True)    # tenths of mm

    station = relationship("WeatherStation", back_populates="observations")


class WeatherStatsYearly(Base):
    """
    Yearly summary per station, computed from WeatherObservation.
    """
    __tablename__ = "weather_stats_yearly"

    station_id = Column(Integer, ForeignKey("weather_station.id"), primary_key=True)
    year = Column(Integer, primary_key=True)

    avg_max_temp_c = Column(Float, nullable=True)   # °C
    avg_min_temp_c = Column(Float, nullable=True)   # °C
    total_precip_cm = Column(Float, nullable=True)  # cm

    station = relationship("WeatherStation", back_populates="stats")
