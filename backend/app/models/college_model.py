from sqlalchemy import Column , Integer , String 
from app.db.database import Base
from sqlalchemy.orm import Relationship


class College(Base):
    __tablename__="colleges"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    college_email=Column(String,nullable=False)
    code=Column(String,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    country=Column(String,nullable=False)

