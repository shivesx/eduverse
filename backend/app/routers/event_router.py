from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.event_model import Event
from app.schemas.event_schemas import CreateEvent,UpdateEvent,EventResponse
from app.security.depen import get_current_user


router=APIRouter(prefix="/events",tags=["Events"])


# get all events

@router.get("/all",response_model=list[EventResponse])
def get_all_events(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Admin access only")
    events=db.query(Event).all()

    return events

# get event by college_id
@router.get("/college/{college_id}",response_model=list[EventResponse])
def get_events_by_college_id(college_id:int,db:Session=Depends(get_db)):

    events=db.query(Event).filter(Event.college_id==college_id).all()

    return events

# get event by event_id
@router.get("/event/{event_id}",response_model=EventResponse)
def get_event_by_event_id(event_id:int,db:Session=Depends(get_db)):

    event=db.query(Event).filter(Event.id==event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    return event

# create event
@router.post("/create",response_model=EventResponse)
def create_event(event:CreateEvent,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Admin access only")
    
    new_event=Event(
        title=event.title,
        descreiption=event.description,
        category=event.category,
        start_time=event.start_time,
        end_time=event.end_time,
        venue=event.venue,
        city=event.city,
        max_participants=event.max_participants,
        organizer=event.organizer,
        college_id=event.college_id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

# update event

@router.patch("/update/{event_id}",response_model=EventResponse)
def update_event(event_id:int,event:UpdateEvent,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Admin access only")

    existing_event=db.query(Event).filter(Event.id==event_id).first()

    if not existing_event:
        raise HTTPException(status_code=404 , detail="Event not found")
    
    for key, value in event.dict(exclude_unset=True).items():
      setattr(existing_event, key, value)

    db.commit()
    db.refresh(existing_event)

    return existing_event


# delete event

@router.delete("/delete/{event_id}")
def delete_event(event_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Admin access only")
    
    event=db.query(Event).filter(Event.id==event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    

    db.delete(event)
    db.commit()

    return {"detail":"Event deleted successfully"}



