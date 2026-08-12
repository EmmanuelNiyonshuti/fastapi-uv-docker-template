import jwt
import pytest

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password


def test_hash_and_verify_password() -> None:
    hashed = hash_password("supersecret")
    assert hashed != "supersecret"
    assert verify_password("supersecret", hashed)
    assert not verify_password("wrong", hashed)


def test_create_access_token_is_decodable() -> None:
    token = create_access_token(subject="42")
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "42"


def test_expired_token_is_rejected() -> None:
    import datetime as dt

    payload = {
        "sub": "1",
        "exp": dt.datetime.now(dt.UTC) - dt.timedelta(minutes=5),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
