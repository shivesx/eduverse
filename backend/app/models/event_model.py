from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from app.db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__="events"

    id=Column(Integer,primary_key=True, index=True)

    title=Column(String,nullable=True)
    descreiption=Column(String,nullable=False)
    category=Column(String,nullable=True)

    start_time=Column(DateTime,nullable=True)
    end_time=Column(DateTime,nullable=True)

    venue=Column(String,nullable=False)
    city=Column(String,nullable=False)

    max_participants=Column(Integer,nullable=True)
    organizer=Column(String,nullable=False)

    college_id=Column(Integer,ForeignKey("colleges.id"),nullable=False)
    
    created_at=Column(DateTime,default=datetime.utcnow)


    # college=relationship("College",back_populates="events")
