from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.database import get_db
from app.core.security import (
    verify_password, 
    create_access_token, 
    decode_access_token
)
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth")

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user through sent credentials"""
    token = credentials.credentials

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("id")

    stmt = select(User).where(User.id==user_id)
    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


@router.post("/login/", tags=["auth"], response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == credentials.email.lower())
    result = await db.execute(stmt)
    
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Credentials did not match"
        )
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    
    data = {
        "id": user.id,
        "email": user.email,
    }

    access_token = create_access_token(data=data)

    return TokenResponse(access_token=access_token)
            

@router.get("/me/", tags=["auth"], response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Return current user using dependency injection"""
    return current_user