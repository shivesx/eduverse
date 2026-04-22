from pydantic import BaseModel,EmailStr

class CollegeCreate(BaseModel):
    name:str
    college_email:EmailStr
    code:int
    city:str
    state:str
    country:str

class CollegeResponse(BaseModel):
    id:int
    name:str
    college_email:EmailStr
    code:int
    city:str
    state:str
    country:str

