from datetime import datetime
from enum import StrEnum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.types import DateTime
from typing import Optional

from app.core.database import Base


class UserRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True,)
    hashed_password: Mapped[str]
    first_name: Mapped[Optional[str]] = mapped_column(default=None)
    last_name: Mapped[Optional[str]] = mapped_column(default=None)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), 
        default=UserRole.ADMIN
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),default=None
    )

    @validates('email')
    def normalize_email(self, key, email):
        return email.lower() if email else email

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    def is_super_admin(self) -> bool:
        return self.role == UserRole.SUPER_ADMIN

