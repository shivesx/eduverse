from sqlalchemy import Column, Integer,String,Float,ForeignKey,DateTime
from app.db.database import Base
from datetime import datetime


class Fees(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)

    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    remaining_amount = Column(Float, nullable=False)

    fees_type = Column(String, nullable=False)

    status = Column(String, default="pending")

    due_date = Column(DateTime, nullable=False)

    semester = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    
