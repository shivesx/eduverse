from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate
from app.schemas.token_schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.security.jwt import create_access_token
from passlib.context import CryptContext
import random
from app.security.email import send_otp_email
from app.schemas.otp_verification import VerifyOTP
from app.schemas.google_login import GoogleAuth
from app.security.google import verify_google_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp():
    return str(random.randint(100000, 999999))


# 🔐 VERIFY OTP
@router.post("/verify-otp")
def verify_otp(data: VerifyOTP, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email.lower()).first()

    if not user:
        raise HTTPException(404, "User not found")

    if user.otp_attempts >= 5:
        raise HTTPException(403, "Too many attempts. Try later")

    if user.otp != data.otp:
        user.otp_attempts += 1
        db.commit()
        raise HTTPException(400, "Invalid OTP")

    if not user.otp_expiry or user.otp_expiry < datetime.utcnow():
        raise HTTPException(400, "OTP Expired")

    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    user.otp_attempts = 0

    db.commit()

    return {"message": "OTP Verified Successfully"}


# 📝 SIGNUP (with resend logic)
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    email = user.email.lower()
    existing_user = db.query(User).filter(User.email == email).first()

    otp = generate_otp()

    # 👉 अगर user already exist करता है
    if existing_user:

        if existing_user.is_verified:
            raise HTTPException(400, "Email already registered")

        # 🔁 RESEND OTP
        existing_user.otp = otp
        existing_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        existing_user.otp_attempts = 0

        db.commit()

        send_otp_email(existing_user.email, otp)

        return {"message": "OTP resent to your email"}

    # 👉 new user
    hashed = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=email,
        password=hashed,
        otp=otp,
        otp_expiry=datetime.utcnow() + timedelta(minutes=5),
        is_verified=False,
        otp_attempts=0
    )

    db.add(new_user)
    db.commit()

    try:
        send_otp_email(email, otp)
    except Exception as e:
        db.delete(new_user)
        db.commit()
        raise HTTPException(500, f"Email send failed: {str(e)}")

    return {"message": "OTP sent to your email"}


# 🔑 LOGIN
@router.post("/login", response_model=Token)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.username.lower()).first()

    if not user:
        raise HTTPException(400, "Invalid Credentials")

    if not user.is_verified:
        raise HTTPException(403, "Please verify your email first")

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(400, "Invalid Credentials")

    access_token = create_access_token({"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }


# google login


@router.post("/google-login", response_model=Token)
def google_login(data: GoogleAuth, db: Session = Depends(get_db)):

    # 🔍 Verify token with Google
    payload = verify_google_token(data.token)

    if not payload:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    # 📧 Get user data from Google
    email = payload.get("email")
    name = payload.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google token")

    email = email.lower()

    # 🔎 Check if user exists
    user = db.query(User).filter(User.email == email).first()

    # 🆕 Create new user if not exists
    if not user:
        user = User(
            name=name,
            email=email,
            password="",  # dummy password
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 🔐 Generate JWT
    access_token = create_access_token({"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }