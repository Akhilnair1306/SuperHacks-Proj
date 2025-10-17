from pydantic import BaseModel, EmailStr

class JiraConnectRequest(BaseModel):
    jira_domain: str
    jira_email: EmailStr
    jira_api_token: str


class ProjectCreateRequest(BaseModel):
    name: str
    key: str
    lead_account_id: str
    project_type: str = "software"
    template_key: str = "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic"