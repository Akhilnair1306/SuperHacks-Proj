# services/user_service.py
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.database import get_db
from sqlalchemy.orm import Session
from app.services.auth import hash_password

def create_user(user: UserCreate, db: Session):
    """Create a new user with hashed password"""
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        system_role=user.system_role.value,
        # functional_role=user.functional_role.value,
        phone_number=user.phone_number,
        status=user.status,
        profile_completed=user.profile_completed,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()