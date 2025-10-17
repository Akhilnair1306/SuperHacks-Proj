from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    technician = "technician"
    
class UserBase(BaseModel):
    username: str
    email: EmailStr
    system_role: UserRole = UserRole.technician
    # functional_role: Optional[FunctionalRole] = None
    phone_number: Optional[str] = None
    status: str = "active"
    profile_completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    system_role: UserRole
    # functional_role: Optional[FunctionalRole] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class TechnicianMetricsResponse(BaseModel):
    user_id: uuid.UUID
    total_tickets: int
    avg_resolution_time: float
    sla_compliance_rate: float
    current_load: int
    last_active: Optional[datetime] = None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
