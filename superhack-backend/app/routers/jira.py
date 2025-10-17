from fastapi import APIRouter, Depends
from app.schemas.jira import JiraConnectRequest, ProjectCreateRequest
from app.services.database import get_db
from app.services.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.jira_service import connect_to_jira,create_jira_project


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/connect")
def connect_jira(request: JiraConnectRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return connect_to_jira(request,db, current_user)

@router.post("/create-project")
def create_project( request: ProjectCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_jira_project(request,db, current_user)