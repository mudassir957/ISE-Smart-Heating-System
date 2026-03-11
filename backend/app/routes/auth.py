from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Prototype rule: first user becomes admin
    role = "admin" if crud.count_users(db) == 0 else "user"
    user = crud.create_user(
        db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=role,
    )
    return user

@router.post("/login", response_model=schemas.TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses "username" field — we treat it as email
    user = crud.get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    return schemas.TokenOut(access_token=token)

@router.get("/me", response_model=schemas.UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user