from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    subject = Column(String, nullable=False)

    total_marks = Column(Integer, nullable=True)
    obtained_marks = Column(Integer, nullable=True)

    assigned_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)

    file_url = Column(String, nullable=True)

    user_assignment_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    