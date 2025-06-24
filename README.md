### Payroll


#### Run

```Set Up Environment
    python -m venv venv
```
```Activate environment
    source venv/bin/activate
```
```Install dependencies
    pip install -r requirements.txt
```
```run command
    uvicorn app.main:app --reload --port 8001
```

```packages
    pip install celery[redis]
    pip install "celery[redis]" "celery[beat]"
    celery -A app.core.celery_worker.celery_app beat --loglevel=info

```

#### Features
- FastAPI
- Postgresql
- SQLAlchemy
- Albemic
- JWT
- Models (User, payroll)
- CRUD (User, payroll)
- Role based permission
- Celery

#### Features next

- More filer on Payroll list
