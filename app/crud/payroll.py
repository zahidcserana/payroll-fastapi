from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payroll import Payroll
from app.schemas.payroll import PayrollCreate


def create_payroll(db: Session, employee_id: int, data: PayrollCreate):
    existing = db.query(Payroll).filter_by(employee_id=employee_id, month=data.month).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payroll already exists for this employee and month")

    net_salary = data.salary + data.bonus - data.tax
    record = Payroll(
        employee_id=employee_id,
        month=data.month,
        salary=data.salary,
        bonus=data.bonus,
        tax=data.tax,
        net_salary=net_salary,
        date_generated=data.date_generated,
        remarks=data.remarks  # ✅ Include remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_payrolls_by_employee(db: Session, employee_id: int):
    return db.query(Payroll).filter(Payroll.employee_id == employee_id).all()


def get_all_payrolls(db: Session):
    return db.query(Payroll).all()
