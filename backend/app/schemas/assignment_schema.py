from pydantic import BaseModel

class CreateAssignment(BaseModel):
    title: str
    description: str
    subject: str
    total_marks: int
    obtained_marks: int
    due_date: str
    file_url: str
    user_assignment_id: int


class UpdateAssignment(BaseModel):
    title: str
    description: str
    subject: str
    total_marks: int
    obtained_marks: int
    due_date: str
    file_url: str
    user_assignment_id: int


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    total_marks: int
    obtained_marks: int
    assigned_date: str
    due_date: str
    file_url: str
    user_assignment_id: int
    created_at: str