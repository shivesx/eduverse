from fastapi import APIRouter,Depends,HTTPException,Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.subject_model import Subject
from app.schemas.subject_schemas import SubjectCreate,SubjectResponse
from app.security.depen import get_current_user
from datetime import datetime


router=APIRouter(prefix="/subject",tags=["Subject"])


# get all subjects

@router.get("/all",response_model=list[SubjectResponse])
def get_all_subject( current_user=Depends(get_current_user), db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")

    subjects=db.query(Subject).all()

    if not subjects:
        raise HTTPException(status_code=404,detail="No subject found")

    return subjects


# get subject by id 

@router.get("/{subject_id}",response_model=SubjectResponse)
def get_subject_by_id(subject_id:int ,current_user=Depends(get_current_user), db:Session=Depends(get_db)):

    subject=db.query(Subject).filter(Subject.id==subject_id).first()

    if not subject:
        raise HTTPException(status_code=404,detail="Subject not found!")
    
    return subject


# add subject

@router.post("/add",response_model=SubjectCreate)
def add_subject(subject:SubjectCreate,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")

    new_subject=Subject(
        name=subject.name,
        code=subject.code,
        semester=subject.semester,
        college_id=subject.college_id,
        credits=subject.credits,
        created_at=subject.created_at
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject




# Delete subject

@router.delete("/delete/{subject_id}")
def delete_subject(subject_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")

    subject=db.query(Subject).filter(Subject.id==subject_id).first()

    if not subject:
        raise HTTPException(status_code=404,detail="Subject not found")
    
    db.delete(subject)
    db.commit()

    return {"detail":"Subject deleted successfully"}


# update subject data

@router.patch("/update/{subject_id}",response_model=SubjectResponse)

def update_subject(subject_id:int ,
                   name:str | None=Form(None),
                    code:int | None=Form(None),
                    semester:int | None=Form(None),
                        college_id:int | None=Form(None),
                            credits:int | None=Form(None),
                                created_at:datetime | None=Form(None),
                                    current_user=Depends(get_current_user),
                                        db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")
                 

    subject=db.query(Subject).filter(Subject.id==subject_id).first()

    if not subject:
        raise HTTPException(status_code=404,detail="Subject not found")
    
    if name is not None:
        subject.name = name

    if code is not None:
        subject.code = code

    if semester is not None:
        subject.semester = semester

    if college_id is not None:
        subject.college_id = college_id

    if credits is not None:
        subject.credits = credits

    if created_at is not None:
        subject.created_at = created_at

    db.commit()
    db.refresh(subject)
   

    return subject

