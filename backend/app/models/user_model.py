from sqlalchemy import Column , Integer , String ,Boolean , DateTime
from app.db.database import Base

class User(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    password=Column(String,nullable=False)
    role=Column(String,default="student")
    college_id=Column(Integer,nullable=True)
    enrollment_number=Column(String)
    admission_year=Column(Integer)
    course=Column(String)
    branch=Column(String)
    address=Column(String)


    is_verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    otp_attempts = Column(Integer, default=0)
    # kidhweaakbgxkyoo