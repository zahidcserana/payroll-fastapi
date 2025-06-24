from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.payroll import Payroll
from app.models.user import User


def generate_monthly_payrolls(db: Session):
    today = date.today()
    first_of_this_month = today.replace(day=1)
    last_month = first_of_this_month - timedelta(days=1)
    payroll_month = last_month.replace(day=1)

    employees = db.query(User).filter(User.role == "employee", User.is_active == True).all()

    for employee in employees:
        # Skip if payroll already exists
        existing = db.query(Payroll).filter_by(employee_id=employee.id, month=payroll_month).first()
        if existing:
            continue

        salary = employee.salary or 0
        net_salary = salary  # Add logic for bonus/tax if needed

        payroll = Payroll(
            employee_id=employee.id,
            month=payroll_month,
            salary=salary,
            bonus=0,
            tax=0,
            net_salary=net_salary,
            date_generated=today,
            remarks=f"Auto-generated for {payroll_month.strftime('%B %Y')}"
        )
        db.add(payroll)

    db.commit()
