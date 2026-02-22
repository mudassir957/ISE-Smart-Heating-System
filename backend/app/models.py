from sqlalchemy import Column, Integer, Float, DateTime, Index
import datetime
from .database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    occupancy = Column(Integer, nullable=False)  # 0 = empty, 1 = occupied
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True, nullable=False)

    __table_args__ = (
        Index("ix_sensor_data_timestamp", "timestamp"),
    )