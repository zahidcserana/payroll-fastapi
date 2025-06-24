from celery import Celery

celery_app = Celery(
    "payroll",
    broker="redis://localhost:6379/0",  # or use settings.REDIS_URL
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    timezone="Asia/Dhaka",
    enable_utc=False
)
