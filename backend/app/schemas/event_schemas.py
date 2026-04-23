from pydantic import BaseModel

class CreateEvent(BaseModel):
    title:str
    description:str
    category:str
    start_time:str
    end_time:str
    venue:str
    city:str
    max_participants:int
    organizer:str
    college_id:int
    created_at:str

class UpdateEvent(BaseModel):
    title:str
    description:str
    category:str
    start_time:str
    end_time:str
    venue:str
    city:str
    max_participants:int
    organizer:str
    college_id:int
    created_at:str

class EventResponse(BaseModel):
    id:int
    title:str
    description:str
    category:str
    start_time:str
    end_time:str
    venue:str
    city:str
    max_participants:int
    organizer:str
    college_id:int
    created_at:str
