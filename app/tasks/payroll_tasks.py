from app.core.celery_worker import celery_app
from app.database import SessionLocal
from app.services.payroll_service import generate_monthly_payrolls


@celery_app.task(name="generate_monthly_payrolls")
def generate_monthly_payrolls_task():
    db = SessionLocal()
    try:
        generate_monthly_payrolls(db)
    finally:
        db.close()
