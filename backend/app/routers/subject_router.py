from fastapi import APIRouter,Depends,HTTPException,Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.subject_model import Subject
from app.schemas.subject_schemas import SubjectCreate,SubjectResponse
from app.security.depen import get_current_user


router=APIRouter(prefix="/subject",tags=["Subject"])


# get all subjects

@router.get("/all",response_model=list[SubjectResponse])
def get_all_subject( current_user=Depends(get_current_user), db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")

    subject=db.query(Subject).all()

    if not subject:
        raise HTTPException(status_code=404,detail="No subject found")

    return subject


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
        raise HTTPException(status_code=404,detail="College not found")
    
    db.delete(subject)
    db.commit()

    return {"detail":"Subject deleted successfully"}


# update subject data

@router.patch("/update/{college_id}",response_model=SubjectResponse)

def update_college(college_id:int ,
                   name:str | None=Form(None),
                    college_email:str | None=Form(None),
                     code:str | None=Form(None),
                        city:str | None=Form(None),
                            state:str | None=Form(None),
                                country:str | None=Form(None),
                                    current_user=Depends(get_current_user),
                                        db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=401, detail="Only Admin Access!")
                 

    college=db.query(College).filter(College.id==college_id).first()

    if not college:
        raise HTTPException(status_code=404,detail="College not found")
    
    if name is not None:
        college.name = name

    if college_email is not None:
        college.college_email = college_email

    if code is not None:
        college.code = code

    if city is not None:
        college.city = city

    if state is not None:
        college.state = state

    if country is not None:
        college.country = country

    db.commit()
    db.refresh(college)
   

    return college

