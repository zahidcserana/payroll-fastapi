from datetime import date

from pydantic import BaseModel


class PayrollCreate(BaseModel):
    month: str
    salary: float
    bonus: float = 0
    tax: float = 0
    date_generated: date


class PayrollOut(PayrollCreate):
    id: int
    net_salary: float
    employee_id: int

    class Config:
        orm_mode = True
