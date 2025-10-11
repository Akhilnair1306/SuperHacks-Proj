from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, get_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
def register_user(user: UserCreate):
    return create_user(user)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
