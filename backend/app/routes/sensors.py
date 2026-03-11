from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user  # optional protection

router = APIRouter(prefix="/sensors", tags=["sensors"])

WINDOWS = {
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "7d": timedelta(days=7),
}

@router.get("/recent", response_model=list[schemas.SensorDataOut])
def get_recent(
    limit: int = Query(10, ge=1, le=500),
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user),  # uncomment if you want auth required
):
    return crud.get_recent_data(db, limit=limit)

@router.get("/history", response_model=list[schemas.SensorDataOut])
def get_history(
    window: str = Query("1h", pattern="^(1h|1d|7d)$"),
    limit: int = Query(5000, ge=1, le=200000),
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    since = datetime.utcnow() - WINDOWS[window]
    return crud.get_data_since(db, since=since, limit=limit)

@router.get("/summary", response_model=schemas.SensorSummaryOut)
def get_summary(
    window: str = Query("1h", pattern="^(1h|1d|7d)$"),
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    since = datetime.utcnow() - WINDOWS[window]
    s = crud.get_summary_since(db, since=since)
    count = s["count"]
    occupancy_rate = (s["occupied_count"] / count) if count else 0.0
    return schemas.SensorSummaryOut(
        window=window,
        count=count,
        temp_min=s["temp_min"],
        temp_max=s["temp_max"],
        temp_avg=s["temp_avg"],
        occupied_count=s["occupied_count"],
        empty_count=s["empty_count"],
        occupancy_rate=occupancy_rate,
    )