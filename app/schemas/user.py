from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "employee"  # default to employee


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True


class UserPayrollOut(BaseModel):
    id: int
    email: str
    role: str
    salary: float
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    salary: Optional[float] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class SalaryUpdateItem(BaseModel):
    employee_id: int
    salary: float
