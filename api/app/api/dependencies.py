from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import User, UserRole
from app.core.database import get_db
from app.core.security import decode_access_token
from app.services.auth_service import AuthService

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db = Depends(get_db)
) -> User:
    """Get current authenticated user using the Authorization header"""
    token = credentials.credentials

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("id")
    user = await AuthService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require user to be admin or super_admin."""
    if current_user.role not in (UserRole.SUPER_ADMIN, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require user to be super_admin."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Super admin access required")
    return current_user