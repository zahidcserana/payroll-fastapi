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

#### Base Features
- FastAPI
- Postgresql
- SQLAlchemy
- Albemic
- JWT
- Models (User, payroll)
- CRUD (User, payroll)
- Role based permission 