from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me/preferences", response_model=schemas.PreferencesOut)
def get_my_preferences(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    prefs = crud.get_preferences(db, current_user.id)
    return prefs

@router.put("/me/preferences", response_model=schemas.PreferencesOut)
def update_my_preferences(
    patch: schemas.PreferencesUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.update_preferences(db, current_user.id, patch)