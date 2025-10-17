from sqlalchemy import Column, Integer, String,Enum, DateTime, Boolean,ForeignKey, JSON, Float
from app.services.database import Base
from sqlalchemy.sql import func
import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class UserRole(enum.Enum):
    admin = "admin"
    technician = "technician"
    manager = "manager"
    
# class FunctionalRole(enum.Enum):
#     FRONTEND_DEV = "FRONTEND_DEV"
#     BACKEND_DEV = "BACKEND_DEV"
#     NETWORK_ENGINEER = "NETWORK_ENGINEER"
#     DATABASE_ADMIN = "DATABASE_ADMIN"
#     HARDWARE_SUPPORT = "HARDWARE_SUPPORT"
#     SECURITY_ANALYST = "SECURITY_ANALYST"
#     GENERAL_SUPPORT = "GENERAL_SUPPORT"
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    system_role = Column(Enum(UserRole), default=UserRole.technician)
    # functional_role = Column(Enum(FunctionalRole), nullable=True)
    phone_number = Column(String)
    status = Column(String, default="active")
    profile_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())

    jira_connection = relationship("JiraConnection", back_populates ="user", uselist= False)
    jira_project = relationship("JiraProject", back_populates= "user")

class TechnicianMetrics(Base):
    __tablename__ = "technician_metrics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    total_tickets = Column(Integer, default=0)
    avg_resolution_time = Column(Float, default=0)
    sla_compliance_rate = Column(Float, default=0)
    current_load = Column(Integer, default=0)
    last_active = Column(DateTime(timezone=True))

class UserActivityLog(Base):
    __tablename__ = "user_activity_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    action = Column(String)
    activity_metadata = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ManagerMetrics(Base):
    __tablename__ = "manager_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    total_technicians = Column(Integer, default=0)
    total_tickets_managed = Column(Integer, default=0)
    avg_team_resolution_time = Column(Float, default=0)
    avg_team_sla_compliance = Column(Float, default=0)

    open_tickets = Column(Integer, default=0)
    closed_tickets = Column(Integer, default=0)
    escalation_rate = Column(Float, default=0)  # % of tickets escalated
    # team_productivity_index = Column(Float, default=0)  # custom score

    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ManagerTeam(Base):
    __tablename__ = "manager_team"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    technician_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))