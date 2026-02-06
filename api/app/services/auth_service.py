from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import verify_password, create_access_token


class AuthService:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def update_user_last_login(db: AsyncSession, user: User) -> None:
        user.last_login = datetime.now(timezone.utc)
        await db.commit()

        return

    @staticmethod
    async def login_user(db: AsyncSession, email: str, password: str) -> str | None:
        user = await AuthService.get_user_by_email(db, email)

        if not user:
            raise Exception("Credentials did not match")

        if not verify_password(password, user.hashed_password):
            raise Exception("Credentials did not match")

        # Update user's last login datetime
        await AuthService.update_user_last_login(db, user)

        data = {
            "id": user.id,
            "email": user.email,
        }

        return create_access_token(data=data)
