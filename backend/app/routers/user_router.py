from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import User
from app.security.depen import get_current_user


router=APIRouter(prefix="/users",tags=["Users"])


@router.get("/me")
def get_my_data(current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    user=db.query(User).filter(User.id==current_user.id).first()

    if not user:
        raise HTTPException(404,"User Not Found")
    
    return{
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "role":user.role,
        "college_id":user.college_id,
        "enrollment_number":user.enrollment_number,
        "admission_year":user.admission_year,
        "course":user.course,
        "branch":user.branch,
        "address":user.address
    }


