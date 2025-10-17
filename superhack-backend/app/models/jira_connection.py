from sqlalchemy import Column, Integer,String, Enum,ForeignKey
from app.services.database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

class JiraConnection(Base):
    __tablename__ = "jira_connection"
    id = Column(UUID(as_uuid=True), primary_key= True, default= uuid.uuid4)
    jira_domain = Column(String, unique = True, index = True)
    jira_email = Column(String, nullable= False)
    jira_api_token = Column(String, nullable= False)
    user_id = Column(UUID(as_uuid= True), ForeignKey("users.id", ondelete= "CASCADE"))
    jira_project = relationship("JiraProject", back_populates= "jira_connection")
    user = relationship("User", back_populates="jira_connection")
    

