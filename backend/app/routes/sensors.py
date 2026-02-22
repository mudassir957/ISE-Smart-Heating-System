from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud, database, schemas

router = APIRouter(prefix="/sensors", tags=["sensors"])

WINDOWS = {
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "7d": timedelta(days=7),
}


@router.get("/recent", response_model=list[schemas.SensorDataOut])
def get_recent(
    limit: int = Query(10, ge=1, le=500),
    db: Session = Depends(database.get_db),
):
    return crud.get_recent_data(db, limit=limit)


@router.get("/history", response_model=list[schemas.SensorDataOut])
def get_history(
    window: str = Query("1h", pattern="^(1h|1d|7d)$"),
    limit: int = Query(5000, ge=1, le=200000),
    db: Session = Depends(database.get_db),
):
    since = datetime.utcnow() - WINDOWS[window]
    return crud.get_data_since(db, since=since, limit=limit)