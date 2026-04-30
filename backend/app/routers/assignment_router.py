from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.assignment_model import Assignment
from app.schemas.assignment_schema import CreateAssignment, UpdateAssignment, AssignmentResponse
from app.security.depen import get_current_user


router = APIRouter(prefix="/assignments", tags=["Assignments"])


# get all assignments

@router.get("/all", response_model=list[AssignmentResponse])
def get_all_assignments(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    assignments = db.query(Assignment).all()
    return assignments



# get assignment by assignment_id

@router.get("/assignment/{assignment_id}", response_model=AssignmentResponse)
def get_assignment_by_id(assignment_id: int, db: Session = Depends(get_db)):

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return assignment


# create assignment (teacher only)

@router.post("/create", response_model=CreateAssignment)
def create_assignment(assignment: CreateAssignment, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")

    new_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        subject=assignment.subject,
        total_marks=assignment.total_marks,
        obtained_marks=assignment.obtained_marks,
        due_date=assignment.due_date,
        file_url=assignment.file_url,
        user_assignment_id=assignment.user_assignment_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


# update assignment (teacher only)

@router.patch("/update/{assignment_id}", response_model=UpdateAssignment)
def update_assignment(assignment_id: int, assignment: UpdateAssignment, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update assignments")

    existing_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not existing_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for key, value in assignment.dict(exclude_unset=True).items():
        setattr(existing_assignment, key, value)

    db.commit()
    db.refresh(existing_assignment)

    return existing_assignment


# delete assignment (teacher only)

@router.delete("/delete/{assignment_id}")
def delete_assignment(assignment_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete assignments")

    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()

    return {"detail": "Assignment deleted successfully"}