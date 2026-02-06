import bcrypt
import jwt
import logging

from datetime import datetime, timedelta, timezone

from app.core.config import settings

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # If no custom token expiration provided, use default from settings
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add token expiration in the payload
    data["exp"] = datetime.now(tz=timezone.utc) + expires_delta

    try:
        return jwt.encode(
            payload=data, key=settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM
        )
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise


def decode_access_token(token: str) -> dict | None:
    try:
        decoded = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=settings.ACCESS_TOKEN_ALGORITHM
        )
        return decoded
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.warning(f"Token validation failed: {e}")
        return None
