from fastapi import APIRouter,Depends,HTTPException,Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.college_model import College
from app.schemas.college_schemas import CollegeResponse,CollegeCreate
from app.security.depen import get_current_user


router=APIRouter(prefix="/college",tags=["College"])


# get all colleges 

@router.get("/all",response_model=list[CollegeResponse])
def get_all_college( current_user=Depends(get_current_user), db:Session=Depends(get_db)):
    
    if current_user.role!="admin":
        raise HTTPException(status_code=401, detail="Only Admin Access!")

    college=db.query(College).all()

    if not college:
        raise HTTPException(status_code=404,detail="No college found")

    return college


# get college by id 

@router.get("/{college_id}",response_model=CollegeResponse)
def get_college_by_id(college_id:int ,current_user=Depends(get_current_user), db:Session=Depends(get_db)):

    college=db.query(College).filter(College.id==college_id).first()

    if not college:
        raise HTTPException(status_code=404,detail="College not found")
    
    return college


# add college

@router.post("/add",response_model=CollegeCreate)
def add_college(college:CollegeCreate,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=401, detail="Only Admin Access!")

    new_college=College(
        name=college.name,
        college_email=college.college_email,
        code=college.code,
        city=college.city,
        state=college.state,
        country=college.country
    )

    db.add(new_college)
    db.commit()
    db.refresh(new_college)

    return new_college




# Delete college

@router.delete("/delete/{college_id}")
def delete_college(college_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=401, detail="Only Admin Access!")

    college=db.query(College).filter(College.id==college_id).first()

    if not college:
        raise HTTPException(status_code=404,detail="College not found")
    
    db.delete(college)
    db.commit()

    return {"detail":"College deleted successfully"}


# update college data

@router.patch("/update/{college_id}",response_model=CollegeResponse)

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
    
    if name:
        college.name = name

    if college_email:
        college.college_email = college_email

    if code:
        college.code = code

    if city:
        college.city = city

    if state:
        college.state = state

    if country:
        college.country = country

    db.commit()
    db.refresh(college)
   

    return college

