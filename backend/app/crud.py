from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from datetime import datetime
from . import models, schemas

# ---------- Sensors ----------
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
    return (
        db.query(models.SensorData)
        .filter(models.SensorData.timestamp >= since)
        .order_by(asc(models.SensorData.timestamp))
        .limit(limit)
        .all()
    )

def get_summary_since(db: Session, since: datetime):
    q = db.query(models.SensorData).filter(models.SensorData.timestamp >= since)

    count = q.count()
    if count == 0:
        return dict(count=0, temp_min=None, temp_max=None, temp_avg=None, occupied_count=0, empty_count=0)

    temp_min, temp_max, temp_avg = db.query(
        func.min(models.SensorData.temperature),
        func.max(models.SensorData.temperature),
        func.avg(models.SensorData.temperature),
    ).filter(models.SensorData.timestamp >= since).one()

    occupied_count = q.filter(models.SensorData.occupancy == 1).count()
    empty_count = count - occupied_count

    return dict(
        count=count,
        temp_min=float(temp_min) if temp_min is not None else None,
        temp_max=float(temp_max) if temp_max is not None else None,
        temp_avg=float(temp_avg) if temp_avg is not None else None,
        occupied_count=occupied_count,
        empty_count=empty_count,
    )

# ---------- Users ----------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def count_users(db: Session):
    return db.query(models.User).count()

def create_user(db: Session, email: str, hashed_password: str, role: str = "user"):
    user = models.User(email=email, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)

    # create default preferences
    prefs = models.UserPreferences(user_id=user.id)
    db.add(prefs)
    db.commit()

    db.refresh(user)
    return user

def list_users(db: Session, limit: int = 200):
    return db.query(models.User).order_by(models.User.created_at.desc()).limit(limit).all()

def set_user_role(db: Session, user_id: int, role: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    user.role = role
    db.commit()
    db.refresh(user)
    return user

# ---------- Preferences ----------
def get_preferences(db: Session, user_id: int):
    return db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()

def update_preferences(db: Session, user_id: int, patch: schemas.PreferencesUpdate):
    prefs = get_preferences(db, user_id)
    if not prefs:
        prefs = models.UserPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    if patch.default_window is not None:
        prefs.default_window = patch.default_window
    if patch.poll_ms is not None:
        prefs.poll_ms = patch.poll_ms
    if patch.theme is not None:
        prefs.theme = patch.theme

    db.commit()
    db.refresh(prefs)
    return prefs