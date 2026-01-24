from fastapi import APIRouter, Depends, HTTPException
from logging import getLogger

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, 
    TokenResponse, 
    UserResponse
)
from app.services.auth_service import AuthService

logger = getLogger(__name__)

router = APIRouter(prefix="/auth")


@router.post("/login/", tags=["auth"], response_model=TokenResponse)
async def login(credentials: LoginRequest, db = Depends(get_db)):
    try:
        access_token = await AuthService.login_user(db, credentials.email, credentials.password)
        logger.info(f"Attempting login with email {credentials.email}")
    except Exception as e:
        logger.warning(f"Login failed: {e}")
        raise HTTPException(
            status_code=403, 
            detail=f"Login failed: {e}"
        )
    logger.info(f"Successful login with email {credentials.email}")

    return TokenResponse(access_token=access_token)
            

@router.get("/me/", tags=["auth"], response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Return current user using dependency injection"""
    return current_user
