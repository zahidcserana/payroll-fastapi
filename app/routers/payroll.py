from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.auth.jwt import SECRET_KEY, ALGORITHM
from app.crud import payroll as crud_payroll
from app.database import get_db
from app.models.user import User
from app.schemas.payroll import PayrollCreate, PayrollOut

router = APIRouter(prefix="/payrolls", tags=["payroll"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/", response_model=PayrollOut)
def create(
        data: PayrollCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create payrolls")
    return crud_payroll.create_payroll(db, current_user.id, data)


@router.get("/my", response_model=List[PayrollOut])
def my_payrolls(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud_payroll.get_payrolls_by_employee(db, current_user.id)


@router.get("/", response_model=List[PayrollOut])
def all_payrolls(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud_payroll.get_all_payrolls(db)
