from fastapi import Depends, HTTPException, status
from typing import List
from app.auth.jwt import get_current_user
from app.models.user import User

def require_role(allowed_roles: List[str]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return user
    return role_checker
