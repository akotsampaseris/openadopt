import asyncio
from getpass import getpass

from app.core.database import async_session_maker
from app.core.security import hash_password
from app.models.user import User, UserRole


async def create_super_admin():
    print("Create Super Admin")
    print("-" * 30)

    email = input("Email: ")
    password = getpass("Password: ")
    first_name = input("First Name (optional): ") or None
    last_name = input("Last Name (optional): ") or None

    async with async_session_maker() as db:
        # Check if user exists
        from sqlalchemy import select

        result = await db.execute(select(User).where(User.email == email.lower()))
        if result.scalar_one_or_none():
            print("User already exists!")
            return

        # Create user
        user = User(
            email=email.lower(),
            hashed_password=hash_password(password),
            first_name=first_name,
            last_name=last_name,
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )

        db.add(user)
        await db.commit()

        print(f"✓ Super admin created: {email}")


def main():
    asyncio.run(create_super_admin())


if __name__ == "__main__":
    asyncio.run(create_super_admin())
