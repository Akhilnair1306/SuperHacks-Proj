from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.services.database import Base
import uuid 
from sqlalchemy.orm import relationship

class JiraProject(Base):
    __tablename__ = "jira_project"

    id = Column(UUID(as_uuid= True), primary_key= True, default= uuid.uuid4)
    jira_connection_id = Column(UUID(as_uuid = True), ForeignKey("jira_connection.id", ondelete= "CASCADE"))
    user_id = Column(UUID(as_uuid= True), ForeignKey("users.id"))
    project_key= Column(String, nullable= False, unique= True)
    project_name = Column(String, nullable= False)
    lead_account_id = Column(String, nullable= False)

    jira_connection = relationship("JiraConnection", back_populates= "jira_project")
    user = relationship("User", back_populates= "jira_project")