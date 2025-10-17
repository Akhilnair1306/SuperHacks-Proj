from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, LoginRequest
from app.services.user_service import create_user, get_user
from app.services.auth import verify_password,create_access_token
from app.services.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user,db)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user  = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )
    access_token = create_access_token(data = {"sub": str(user.id)}, expires_delta= timedelta(hours = 6))
    return {"access_token": access_token,"token_type": "bearer", "role": user.system_role}