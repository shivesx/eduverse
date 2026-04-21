from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserLogin,UserCreate
from app.schemas.token_schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.security.jwt import decode_token,create_access_token
from passlib.context import CryptContext


router=APIRouter(prefix="/auth",tags=["Authentication"])

# for password hashing
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


# signup user


@router.post("/signup")
def signup(user:UserCreate,db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.email==user.email).first()

    if existing_user:
        raise HTTPException(400,"Email already registered")
    
    hashed=pwd_context.hash(user.password)

    new_user=User(
        name=user.name,
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {"message":"User created successfully"}



# login user

@router.post("/login",response_model=Token)
def login(data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(User).filter(User.email==data.username).first()

    if not user:
        raise HTTPException(400,"Invalid Credentials")
    
    if not pwd_context.verify(data.password,str(user.password)):
        raise HTTPException(400,"Invalid Credentials")
    
    access_token=create_access_token({"user_id":user.id})

    return {
        "access_token":access_token,
        "token_type":"bearer",
        "user_id":user.id
        }



