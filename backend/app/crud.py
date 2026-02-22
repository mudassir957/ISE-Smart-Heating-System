from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from datetime import datetime
from . import models, schemas


def create_sensor_data(db: Session, data: schemas.SensorDataCreate):
    db_data = models.SensorData(
        temperature=data.temperature,
        occupancy=data.occupancy,
        timestamp=data.timestamp or datetime.utcnow(),
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_recent_data(db: Session, limit: int = 10):
    return (
        db.query(models.SensorData)
        .order_by(desc(models.SensorData.timestamp))
        .limit(limit)
        .all()
    )


def get_data_since(db: Session, since: datetime, limit: int = 5000):
    # oldest -> newest (best for charts)
    return (
        db.query(models.SensorData)
        .filter(models.SensorData.timestamp >= since)
        .order_by(asc(models.SensorData.timestamp))
        .limit(limit)
        .all()
    )