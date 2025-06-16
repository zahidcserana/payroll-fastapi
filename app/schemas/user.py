from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "employee"  # default to employee

class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True