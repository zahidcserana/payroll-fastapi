from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    month = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    bonus = Column(Float, default=0)
    tax = Column(Float, default=0)
    net_salary = Column(Float, nullable=False)
    date_generated = Column(Date, nullable=False)

    employee = relationship("User", back_populates="payrolls")