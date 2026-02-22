from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SensorDataCreate(BaseModel):
    temperature: float
    occupancy: int
    timestamp: Optional[datetime] = None  # allow DB/default if not provided


class SensorDataOut(BaseModel):
    id: int
    temperature: float
    occupancy: int
    timestamp: datetime

    class Config:
        from_attributes = True  # Pydantic v2