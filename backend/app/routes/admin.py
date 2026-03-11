from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..auth import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[schemas.UserOut])
def admin_list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return crud.list_users(db)

@router.patch("/users/{user_id}/role", response_model=schemas.UserOut)
def admin_set_role(
    user_id: int,
    payload: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    user = crud.set_user_role(db, user_id, payload.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user