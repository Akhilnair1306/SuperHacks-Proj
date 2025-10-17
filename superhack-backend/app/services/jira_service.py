import requests
from fastapi import HTTPException, status
from app.models.jira_connection import JiraConnection
from app.models.jira_projects import JiraProject

def connect_to_jira(request,db,current_user):
    jira_url = f"https://{request.jira_domain}.atlassian.net/rest/api/3/myself"
    auth = (request.jira_email, request.jira_api_token)

    response  = requests.get(jira_url, auth = auth, headers= {"Accept": "application/json"})

    if response.status_code != 200:
        try:
            # Attempt to parse JSON response
            error_detail = response.json()
        except ValueError:
            # If not JSON, fallback to raw text
            error_detail = response.text

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Failed to connect to Jira", "jira_error": error_detail}
        )
    jira_user = response.json()

    jira_integration = JiraConnection(
        user_id=current_user.id,
        jira_email=request.jira_email,
        jira_api_token=request.jira_api_token,  # consider encrypting
        jira_domain=request.jira_domain
    )
    db.add(jira_integration)
    db.commit()

    return {
        "message": "Jira connected successfully",
        "jira_user": jira_user
    }

def create_jira_project(request,db,current_user):
    jira = db.query(JiraConnection).filter(JiraConnection.user_id == current_user.id).first()

    if not jira:
        raise HTTPException(status_code= 400, detail = "User not connected to Jira")
    
    url = f"https://{jira.jira_domain}.atlassian.net/rest/api/3/project"
    payload = {
        "key": request.key,
        "name": request.name,
        "projectTypeKey": request.project_type,
        "projectTemplateKey": request.template_key,
        "leadAccountId": request.lead_account_id
    }
    auth = (jira.jira_email, jira.jira_api_token)
    headers={
        "Accept": "application/json", 
        "Content-Type": "application/json"
        }
    response = requests.post(url, json=payload, auth = auth,headers = headers)

    if response.status_code not in [200, 201]:
        try:
            error_detail = response.json()
        except ValueError:
            error_detail = response.text
        raise HTTPException(status_code=400, detail={"message": "Failed to create",  "jira_error": error_detail})
    # jira_project_details = response.json()
    jira_project = JiraProject(
        jira_connection_id = jira.id,
        user_id = current_user.id,
        project_key= request.key,
        project_name = request.name,
        lead_account_id = request.lead_account_id
    )
    db.add(jira_project)
    db.commit()

    # project_details = requests.get(response_detail.self, auth = auth,headers = headers)
    return {"message": "Project create successfully", "project": response.json()}