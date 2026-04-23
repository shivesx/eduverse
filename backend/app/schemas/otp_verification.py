from pydantic import BaseModel


class VerifyOTP(BaseModel):
    email:str
    otp:str

    