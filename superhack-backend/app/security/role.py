from fastapi import Depends,HTTPException,status
from jose import JWTError, jwt

def require_role(required_roles:list[str]):
    def role_checker(current_user):
        if current_user.system_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker