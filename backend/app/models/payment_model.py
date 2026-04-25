from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.db.database import Base
from datetime import datetime


class Payment(Base):
    __tablename__="payments"

    id=Column(Integer,primary_key=True,index=True)

    fees_id=Column(Integer,ForeignKey("fees.id"),nullable=False)

    amount=Column(Float,nullable=False)
    payment_method=Column(String,nullable=False)
    transaction_id=Column(String,unique=True,nullable=False)
    payment_date=Column(DateTime,default=datetime.utcnow)