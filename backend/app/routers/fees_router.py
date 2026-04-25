from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.fees_schemas import FeesResponse,CreateFees
from app.models.fees_model import Fees
from app.security.depen import get_current_user
from app.models.payment_model import Payment


router=APIRouter(prefix="/fees",tags=["Fees"])


# get my fees

@router.get("/me", response_model=list[FeesResponse])
def get_my_fees(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students allowed")
    

    fees = db.query(Fees).filter(Fees.student_id == current_user.id).all()

    return fees


# get all fees

@router.get("/all",response_model=list[FeesResponse])
def get_all_fees(current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Only Admin Access!")
    
    fees=db.query(Fees).all()
    
   

    return fees

# get fees by id

@router.get("/{fees_id}",response_model=FeesResponse)
def get_fees_by_id(fees_id: int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Only Admin Access!")
    
    fees=db.query(Fees).filter(Fees.id==fees_id).first()

    if not fees:
        raise HTTPException(status_code=404, detail="Fees not found")

    return fees

# get fees by student_id

@router.get("/student/{student_id}",response_model=list[FeesResponse])
def get_fees_by_student_id(student_id: int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Only Admin Access!")
    
    fees=db.query(Fees).filter(Fees.student_id==student_id).all()
    if not fees:
        raise HTTPException(status_code=404, detail="Fees not found")
    
    return fees

# add fees

@router.post("/add",response_model=FeesResponse)
def add_fees(fees:CreateFees,current_user=Depends(get_current_user),db:Session=Depends(get_db)):

    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Only Admin access allowed!")
    existing_fees=db.query(Fees).filter(Fees.student_id==fees.student_id,
                                        Fees.semester==fees.semester,
                                        Fees.academic_year==fees.academic_year).first()
    

    if existing_fees:
        raise HTTPException(status_code=400, detail="Fees for this student and semester already exist")
    

    new_fees=Fees(
        student_id=fees.student_id,
        college_id=fees.college_id,
        total_amount=fees.total_amount,
        paid_amount=0.0,
        remaining_amount=fees.total_amount,
        fees_type=fees.fees_type,
        status="pending",
        due_date=fees.due_date,
        semester=fees.semester,
        academic_year=fees.academic_year
    )

    db.add(new_fees)
    db.commit()
    db.refresh(new_fees)

    return new_fees


# delet fees


@router.delete("/{fees_id}")
def delete_fees(fees_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only Admin Access!")

    fees = db.query(Fees).filter(Fees.id == fees_id).first()

    if not fees:
        raise HTTPException(status_code=404, detail="Fees not found")

    # check payment
    payment = db.query(Payment).filter(Payment.fees_id == fees_id).first()

    if payment:
        raise HTTPException(status_code=400, detail="Cannot delete fees with payments")

    db.delete(fees)
    db.commit()

    return {"message": "Fees deleted successfully"}


