from pydantic import BaseModel,DateTime

class SubjectCreate(BaseModel):
    name:str
    code:int
    semester:int
    college_id:int
    credits:int
    created_at:DateTime


class SubjectResponse(BaseModel):
    id:int
    name:str
    code:int
    semester:int
    college_id:int
    credits:int
    created_at:DateTime