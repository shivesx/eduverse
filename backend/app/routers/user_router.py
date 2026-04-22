from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import User
from app.security.depen import get_current_user
from app.schemas.user_schemas import UserResponse,CreateUser,UpdateUser

router=APIRouter(prefix="/users",tags=["Users"])


# get me 

@router.get("/me",response_model=UserResponse)
def get_my_data(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
      raise HTTPException(status_code=404, detail="User not found")


    return user


# delete all users (admin)
    
@router.get("/all",response_model=list[UserResponse])
def get_all_users(current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403 , detail="Only admin access allowed")
    
    users=db.query(User).all()

    return users

# get user by id 

@router.get("/{user_id}",response_model=UserResponse)
def get_user_by_id(user_id:int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403 , detail="Only admin access allowed")

    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404 , detail="User not found")
    
    return user


# get all users (admin)




@router.delete("/delete/all")
def delete_all_users(current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403 , detail="Only admin access allowed")
    
    users=db.query(User).all()

    for user in users:
        db.delete(user)
    
    db.commit()

    return {"message" : "All users deleted successfully"}


# delete user by id 

@router.delete("/delete/{user_id}")
def delete_user_by_id(user_id:int , current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Only admin access allowed")
    
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404 , detail="User not found")
    
    db.delete(user)
    db.commit()

    return {"message" : "User deleted successfully"}


# create user

@router.post("/create", response_model=UserResponse)
def create_user(
    user: CreateUser,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # check already filled
    if current_user.college_id is not None:
        raise HTTPException(status_code=400, detail="Profile already created")

    current_user.college_id = user.college_id
    current_user.enrollment_number = user.enrollment_number
    current_user.admission_year = user.admission_year
    current_user.course = user.course
    current_user.branch = user.branch
    current_user.address = user.address

    db.commit()
    db.refresh(current_user)

    return current_user


# update user 
@router.patch("/update",response_model=UserResponse)
def update_user(user:UpdateUser,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.id==current_user.id).first()
    
    if not existing_user:
       raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
      setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)

    return existing_user

# update user by id (admin)

@router.patch("/update/{user_id}",response_model=UserResponse)
def update_user_by_admin(
    user_id: int,
    user: UpdateUser,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin access allowed")

    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)

    return existing_user





