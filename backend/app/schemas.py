from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

# ---------- Sensors ----------
class SensorDataCreate(BaseModel):
    temperature: float
    occupancy: int
    timestamp: Optional[datetime] = None

class SensorDataOut(BaseModel):
    id: int
    temperature: float
    occupancy: int
    timestamp: datetime

    class Config:
        from_attributes = True

class SensorSummaryOut(BaseModel):
    window: str
    count: int
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    temp_avg: Optional[float] = None
    occupied_count: int
    empty_count: int
    occupancy_rate: float  # occupied_count / count (0..1)

# ---------- Auth / Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Preferences ----------
class PreferencesOut(BaseModel):
    default_window: Literal["1h", "1d", "7d"]
    poll_ms: int
    theme: Literal["light", "dark"]

    class Config:
        from_attributes = True

class PreferencesUpdate(BaseModel):
    default_window: Optional[Literal["1h", "1d", "7d"]] = None
    poll_ms: Optional[int] = Field(default=None, ge=500, le=60000)
    theme: Optional[Literal["light", "dark"]] = None

# ---------- Admin ----------
class RoleUpdate(BaseModel):
    role: Literal["user", "admin"]