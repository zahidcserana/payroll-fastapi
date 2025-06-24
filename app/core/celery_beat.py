from celery.schedules import crontab

from app.core.celery_worker import celery_app

celery_app.conf.beat_schedule = {
    "generate-payrolls-every-month": {
        "task": "generate_monthly_payrolls",
        "schedule": crontab(hour=2, minute=0, day_of_month=5),  # every 5th day at 2 AM
    }
}
