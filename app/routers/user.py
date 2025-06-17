from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.crud import payroll as crud_payroll
from app.crud import user as crud_user
from app.database import get_db
from app.models.user import User
from app.schemas.payroll import PayrollOut
from app.schemas.user import UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{user_id}", response_model=UserOut)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["admin"]))
):
    return crud_user.update_user(db, user_id, user_data)


@router.get("/my_payrolls", response_model=List[PayrollOut])
def my_payrolls(
        current_user: User = Depends(require_role(["employee"])),
        db: Session = Depends(get_db)
):
    return crud_payroll.get_payrolls_by_employee(db, current_user.id)
