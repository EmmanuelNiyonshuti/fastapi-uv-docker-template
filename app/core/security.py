from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

pwd_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    return pwd_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)


def get_access_token_expiration_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRES_AT


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=get_access_token_expiration_minutes())
    payload = {"exp": expires_at, "sub": str(subject)}
    return jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
