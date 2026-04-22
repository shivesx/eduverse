from typing import Optional

from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class CreateUser(BaseModel):
    college_id:int
    enrollment_number:int
    admission_year:int
    course:str
    branch:str
    address:str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    college_id: Optional[int] = None
    enrollment_number: Optional[int] = None
    admission_year: Optional[int] = None
    course: Optional[str] = None
    branch: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    college_id :Optional[int]=None
    enrollment_number:Optional[int]=None
    admission_year:Optional[int]=None
    course:Optional[str]=None
    branch:Optional[str]=None
    address:Optional[str]=None

        