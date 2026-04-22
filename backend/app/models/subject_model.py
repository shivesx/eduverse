from sqlalchemy import Column , Integer , String , DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime


class Subject(Base):
    __tablename__="subjects"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    code=Column(String,unique=True,nullable=False)
    semester=Column(Integer,nullable=False)
    college_id=Column(Integer,nullable=False, ForeignKey="colleges.id")
    credits=Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    