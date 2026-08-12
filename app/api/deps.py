from collections.abc import AsyncGenerator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.config import settings
from app.core.db import async_engine
from app.crud import find_user_by_id

BearerToken = OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_db() -> AsyncGenerator[AsyncConnection]:
    async with async_engine.connect() as conn:
        yield conn


DbConnection = Annotated[AsyncConnection, Depends(get_db)]
AccessToken = Annotated[str, Depends(BearerToken)]


def _credentials_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(db_conn: DbConnection, token: AccessToken) -> Row:
    try:
        payload = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise _credentials_exception("Token has expired") from None
    except jwt.InvalidTokenError:
        raise _credentials_exception("Invalid token") from None

    subject = payload.get("sub")
    if subject is None:
        raise _credentials_exception("Invalid token")

    user = await find_user_by_id(db_conn, int(subject))
    if user is None:
        raise _credentials_exception("User not found")
    return user


CurrentUser = Annotated[Row, Depends(get_current_user)]
