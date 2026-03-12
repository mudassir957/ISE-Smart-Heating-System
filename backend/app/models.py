import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    occupancy = Column(Integer, nullable=False)  # 0/1
    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        index=True,
        nullable=False
    )

#    __table_args__ = (Index("ix_sensor_data_timestamp", "timestamp"),)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")  # "user" | "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    default_window = Column(String, nullable=False, default="1h")  # 1h/1d/7d
    poll_ms = Column(Integer, nullable=False, default=2000)
    theme = Column(String, nullable=False, default="light")  # light/dark

    user = relationship("User", back_populates="preferences")

    __table_args__ = (UniqueConstraint("user_id", name="uq_user_preferences_user_id"),)