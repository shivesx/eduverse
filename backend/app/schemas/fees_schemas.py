from pydantic import BaseModel
from datetime import datetime

class PayFees(BaseModel):
    fees_id: int
    amount: float
    payment_method: str
    transaction_id: str

class CreateFees(BaseModel):
    student_id:int
    college_id:int
    total_amount:float
    fees_type:str
    due_date:datetime
    semester:str
    academic_year:str

class PaymentResponse(BaseModel):
    amount: float
    payment_method: str
    transaction_id: str
    payment_date: datetime


class FeesResponse(BaseModel):
    id: int
    student_id: int
    college_id: int
    total_amount: float
    paid_amount: float
    remaining_amount: float
    fees_type: str
    status: str
    due_date: datetime
    semester: str
    academic_year: str
    created_at: datetime

    payments: list[PaymentResponse] = []

    class Config:
        from_attributes = True

