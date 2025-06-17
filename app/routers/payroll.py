from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.crud import payroll as crud_payroll
from app.database import get_db
from app.models.user import User
from app.schemas.payroll import PayrollCreate, PayrollOut

# router = APIRouter(prefix="/payrolls", tags=["payroll"])
router = APIRouter(
    prefix="/payrolls",
    tags=["payroll"],
    dependencies=[Depends(require_role(["admin"]))]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/", response_model=PayrollOut)
def create(
        data: PayrollCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["admin"]))
):
    return crud_payroll.create_payroll(db, data.employee_id, data)


@router.get("/", response_model=List[PayrollOut])
def all_payrolls(current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    return crud_payroll.get_all_payrolls(db)
