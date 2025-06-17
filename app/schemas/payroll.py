from datetime import date
from typing import Optional

from pydantic import BaseModel


class PayrollCreate(BaseModel):
    employee_id: int
    month: date
    salary: float
    bonus: float = 0
    tax: float = 0
    date_generated: date
    remarks: Optional[str] = None


class PayrollOut(PayrollCreate):
    id: int
    net_salary: float
    employee_id: int

    class Config:
        orm_mode = True
