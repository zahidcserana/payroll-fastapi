from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.roles import require_role
from app.auth.security import verify_password
from app.crud import user as crud_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)


@router.post("/create", response_model=UserOut)
def create(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["admin"]))
):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)


@router.post("/bootstrap_admin", response_model=UserOut)
def bootstrap_admin(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.role == "admin").first()
    if existing:
        raise HTTPException(status_code=403, detail="Admin already exists")
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Must be role='admin'")
    return crud_user.create_user(db, user)


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserOut])
def users(current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    return crud_user.get_users(db)
